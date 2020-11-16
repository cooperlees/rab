#!/usr/bin/env python3

import logging
from abc import ABC, abstractmethod
from socket import AF_INET6
from types import MappingProxyType

from pyroute2.iproute import IPRoute


LOG = logging.getLogger(__name__)


class Check(ABC):
    """Base class for a check to identify if a WAN interface is down"""

    def __init__(self, interface: str) -> None:
        self.interface = interface
        self.interface_id = 0
        self.fails = 0

    @abstractmethod
    def run(self) -> int:
        """Class to run the check"""
        pass


class DefaultRouteCheck(Check):
    def run(self) -> int:
        try:
            with IPRoute() as ipr:
                links = ipr.get_links("all")
                routes = ipr.get_default_routes(family=AF_INET6)
        except Exception as e:
            LOG.exception(f"Failed to get list of valid interfaces: {e}")
            return -1

        for link in links:
            if link.get_attr("IFLA_IFNAME") != self.interface:
                continue

            self.interface_id = link["index"]
            break
        if not self.interface_id:
            LOG.error(f"Unable to find {self.interface} index")
            return 1

        for route in routes:
            multi_routes = route.get_attr("RTA_MULTIPATH")
            for mr in multi_routes:
                if mr["oif"] == self.interface_id:
                    return 0

        return 2


_checks = {
    "default_route_check": DefaultRouteCheck,
}
CHECKS = MappingProxyType(_checks)


if __name__ == "__main__":
    drc = CHECKS["default_route_check"]("ens33")
    print(drc.run())
