#!/usr/bin/env python3

import logging
from typing import Any


LOG = logging.getLogger(__name__)


class RA:
    """Class to generate an RA with lifetime 0 to force devices to
    start using alternate router"""

    def generate(self, interface: str) -> Any:
        """Generate an RA to send with lifetime 0 from interface"""
        return None

    def send(self, interface: str) -> int:
        """Async send an RA out interface to indicate to hosts to stop using Prefix + Route
        - Save waiting for RA expiry"""
        return 0
