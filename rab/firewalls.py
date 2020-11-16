#!/usr/bin/env python3

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import CalledProcessError
from types import MappingProxyType
from typing import Dict, List, Optional, Sequence, Tuple

# Couldn't get to work for nftables with inet tables
# https://github.com/svinota/pyroute2/issues/747
# from pyroute2.nftables.main import NFTables

from rab.utils import gen_check_output


LOG = logging.getLogger(__name__)


class Firewall(ABC):
    """Base class to define the firewall API
    - addRules: Add the RA blocking rule(s)
    - removeRules: Remove the RA blocking rule(s)
    - listRules: Find RA blocking rule(s)
      - Probably used by removed rules"""

    def __init__(self, dryrun: bool = False) -> None:
        self.dryrun = dryrun
        self.dr_pre = ""
        if dryrun:
            self.dr_pre = "[DRYRUN]"

    async def _run_cmd(
        self, cmd: Sequence[str], errors: int = 0, timeout: float = 5
    ) -> Tuple[Optional[bytes], Optional[bytes]]:
        try:
            return await gen_check_output(cmd, timeout=timeout)
        except CalledProcessError as cpe:
            LOG.error(f"{' '.join(cmd)} failed: {cpe} (exit code {cpe.returncode})")
            errors += 1
        except asyncio.TimeoutError as te:
            LOG.error(f"{' '.join(cmd)} timed out: {te}")
            errors += 1

        return (None, None)

    @abstractmethod
    async def addRules(self, interfaces: Optional[str] = None) -> int:
        """Add rules for interfaces + report number of failures or 0 for success"""
        pass

    @abstractmethod
    async def delRules(self, rule_ids: Sequence[int] = ()) -> int:
        """Delete rules for interfaces + report number of failures or 0 for success"""
        pass

    @abstractmethod
    async def listRules(self, interfaces: Optional[str] = None) -> Dict:
        """Get rules and have identifier (e.g. int for nftables) to rule str Dict returned"""
        pass

    @abstractmethod
    async def rulesExist(self) -> Sequence[int]:
        """See if there is an outbound rule for RA blocking"""
        pass


class NftablesCLI(Firewall):
    """nftables via CLI implementation"""

    nft_path = Path("/usr/sbin/nft")
    nft_ra_expr = [
        {
            "match": {
                "op": "==",
                "left": {"payload": {"protocol": "icmpv6", "field": "type"}},
                "right": {"set": [134]},
            }
        },
        {"drop": None},
    ]

    # TODO: Support interfaces
    async def addRules(self, interfaces: Optional[str] = None) -> int:
        errors = 0
        cmd = (
            str(self.nft_path),
            "insert",
            "rule",
            "inet",
            "filter",
            "OUTPUT",
            "position",
            "0",
            "icmpv6",
            "type",
            "{nd-router-advert}",
            "drop",
        )
        if existing_rules := await self.rulesExist():
            existing_rule_count = len(existing_rules)
            LOG.error(f"{existing_rule_count} rules already exist")
            return len(existing_rules)

        LOG.info(f"{self.dr_pre} running '{' '.join(cmd)}'")
        if not self.dryrun:
            self._run_cmd(cmd, errors)
        return errors

    async def delRules(self, rule_ids: Sequence[int] = ()) -> int:
        errors = 0
        for rule_id in rule_ids:
            cmd = (
                str(self.nft_path),
                "delete",
                "rule",
                "inet",
                "filter",
                "OUTPUT",
                "handle",
                str(rule_id),
            )
            LOG.info(f"{self.dr_pre} running '{' '.join(cmd)}'")
            if not self.dryrun:
                await self._run_cmd(cmd, errors)

        return errors

    async def listRules(
        self, interfaces: Optional[str] = None, timeout: float = 2
    ) -> Dict:
        cmd = (
            str(self.nft_path),
            "--json",
            "-n",
            "-a",
            "list",
            "table",
            "inet",
            "filter",
        )
        stdout, stderr = await self._run_cmd(cmd, timeout=timeout)
        if stdout:
            return dict(json.loads(stdout))
        return {}

    async def rulesExist(self) -> Sequence[int]:
        found_rules: List[int] = []
        rule_lists = await self.listRules()
        for fw_data in rule_lists["nftables"]:
            for fw_obj, data in fw_data.items():
                if (
                    fw_obj == "rule"
                    and data["family"] == "inet"
                    and data["table"] == "filter"
                    and data["chain"] == "OUTPUT"
                    and data["expr"] == self.nft_ra_expr
                ):
                    found_rules.append(data["handle"])
        return found_rules


_firewalls = {
    "nftables": NftablesCLI,
}
FIREWALLS = MappingProxyType(_firewalls)


if __name__ == "__main__":
    nft = FIREWALLS["nftables"]()
    rules = asyncio.run(nft.listRules())
    print(json.dumps(rules, indent=2))
