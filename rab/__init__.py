#!/usr/bin/env python3

import asyncio
import argparse
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List

from rab.checks import CHECKS, Check
from rab.firewalls import FIREWALLS, Firewall


LOG = logging.getLogger(__name__)


def _handle_logging(debug: bool) -> None:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-c", "--config", default="/config/rab.json", help="Path of JSON config file"
    )
    parser.add_argument(
        "-D", "--dryrun", action="store_true", help="Don't add Firewall Rule just log"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    return parser.parse_args()


def _read_config(path_str: str) -> Dict:
    config_path = Path(path_str)

    if not config_path.exists():
        LOG.error(f"{config_path} does not exist.")
        return {}

    with config_path.open("r") as cfp:
        return dict(json.load(cfp))


def _validate_config(config: Dict) -> bool:
    if config["firewall"] not in FIREWALLS:
        LOG.error(f"{config['firewall']} is not a valid firewall type")
        return False

    for check in config["checks"]:
        if check not in CHECKS:
            LOG.error(f"{check} is not a valid check")
            return False

    return True


async def _ra_block(
    config: Dict,
    firewall: Firewall,
    interfaces_checks: Dict[str, List[Check]],
    tp: ThreadPoolExecutor,
) -> None:
    loop = asyncio.get_running_loop()
    LOG.info(f"Checking {len(interfaces_checks)} interfaces ...")
    for interface, checks in interfaces_checks.items():
        LOG.info(f"Checking {interface} interface")
        results = await asyncio.gather(
            *[loop.run_in_executor(tp, check.run) for check in checks]
        )
        rules = await firewall.rulesExist()
        # See if any check fails and ensure we have a drop Rule in play
        # Otherwise check if we need to clean it up
        for idx, error in enumerate(results):
            if error:
                # Check if we're already blocked RAs
                if rules:
                    continue

                # Record we've failed
                interfaces_checks[interface][idx].fails += 1
                if interfaces_checks[interface][idx].fails == config["failures"]:
                    check_name = interfaces_checks[interface][idx].__class__.__name__
                    LOG.error(
                        f"{interface} has failed {check_name} "
                        + f"{config['failures']} time. Time to block outgoing RAs"
                    )
                    await firewall.addRules()
            else:
                if interfaces_checks[interface][idx].fails > 0:
                    interfaces_checks[interface][idx].fails -= 1

    # If we have rules added lets check to see if we should clean up
    if rules:
        all_fails = 0
        for interface, checks in interfaces_checks.items():
            all_fails += sum((check.fails for check in checks))

        if all_fails == 0:
            LOG.info("Removing Outgoing RA blocking rule")
            await firewall.delRules(rules)


async def ra_block(
    config: Dict, firewall: Firewall, interfaces_checks: Dict[str, List[Check]]
) -> None:
    tp = ThreadPoolExecutor(max_workers=2, thread_name_prefix="checkers_")
    while True:
        await _ra_block(config, firewall, interfaces_checks, tp)

        LOG.debug(f"Waiting {config['check_interval']}s to recheck interfaces")
        await asyncio.sleep(config["check_interval"])


async def service(args: argparse.Namespace, config: Dict) -> int:
    firewall = FIREWALLS[config["firewall"]](args.dryrun)
    interface_checks: Dict[str, List[Check]] = {}
    for interface in config["wan"]["interfaces"]:
        for check in config["checks"]:
            if interface not in interface_checks:
                interface_checks[interface] = []
            interface_checks[interface].append(CHECKS["check"](interface))

    try:
        await asyncio.gather(ra_block(config, firewall, interface_checks))
    except KeyboardInterrupt:
        pass

    return 0


def main() -> int:
    args = _parse_args()
    _handle_logging(args.debug)

    config_dict = _read_config(args.config)
    if not config_dict:
        return 1

    if not _validate_config(config_dict):
        return 2

    return asyncio.run(service(args, config_dict))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
