#!/usr/bin/env python3

import logging
from abc import ABC, abstractmethod


LOG = logging.getLogger(__name__)


class Check(ABC):
    """Base class for a check to identify if a WAN interface is down"""

    @abstractmethod
    async def run(self) -> int:
        """Class to run the check"""
        pass
