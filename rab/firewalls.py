#!/usr/bin/env python3

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict

from pyroute2.iproute import IPRoute
from pyroute2.nftables.main import NFTables


LOG = logging.getLogger(__name__)


class Firewall(ABC):
    """Base class to define the firewall API
    - addRules: Add the RA blocking rule(s)
    - removeRules: Remove the RA blocking rule(s)
    - listRules: Find RA blocking rule(s)
      - Probably used by removed rules"""

    @abstractmethod
    def addRules(self, interfaces: Optional[str] = None) -> int:
        """Add rules for interfaces + report number of failures or 0 for success"""
        pass

    @abstractmethod
    def delRules(self, interfaces: Optional[str] = None) -> int:
        """Delete rules for interfaces + report number of failures or 0 for success"""
        pass

    @abstractmethod
    def listRules(self, interfaces: Optional[str] = None) -> Dict:
        """Get rules and have identifier (e.g. int for nftables) to rule str Dict returned"""
        pass


class Nftables(Firewall):
    """nftables implementation"""

    def addRules(self, interfaces: Optional[str] = None) -> int:
        pass

    def delRules(self, interfaces: Optional[str] = None) -> int:
        pass

    def listRules(self, interfaces: Optional[str] = None) -> Dict:
        nft = NFTables()
        rules = nft.get_rules()
        with IPRoute() as ipr:
            avail_interfaces = [
                link.get_attr("IFLA_IFNAME") for link in ipr.get_links()
            ]

        print(f"Rules:\n{rules}")
        print(f"Interfaces:\n{avail_interfaces}")
        return {}


if __name__ == "__main__":
    # Testing ...
    nft = Nftables()
    nft.listRules()
