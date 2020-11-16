#!/usr/bin/env python3

import asyncio
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from rab.tests.firewalls import NftablesTests  # noqa: F401
from rab.tests.utils import UtilsTests  # noqa: F401

import rab
from rab.checks import DefaultRouteCheck
from rab.firewalls import NftablesCLI


CONFIG_PATH = Path(__file__).parent.parent.parent / "default_config.json"


class BaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_handle_logging(self) -> None:
        self.assertIsNone(rab._handle_logging(False))

    def test_parse_args(self) -> None:
        self.assertTrue(rab._parse_args())

    def test_read_config_missing(self) -> None:
        self.assertEqual({}, rab._read_config("/tmp/not_there.json"))

    def test_ra_block(self) -> None:
        config = rab._read_config(str(CONFIG_PATH))
        tp = ThreadPoolExecutor(max_workers=2, thread_name_prefix="unittest_")
        test_interface = "eth69"  # should never exist
        test_dryrun_firewall = NftablesCLI(dryrun=True)
        test_default_check = DefaultRouteCheck(test_interface)
        test_interface_checks = {test_interface: [test_default_check]}

        # Test that we run add rule if we hit config['failures']
        test_default_check.fails = 1
        test_dryrun_firewall.addRules = AsyncMock()
        test_dryrun_firewall.rulesExist = AsyncMock(return_value=[])
        self.loop.run_until_complete(
            rab._ra_block(config, test_dryrun_firewall, test_interface_checks, tp)
        )
        self.assertTrue(test_dryrun_firewall.addRules.called)

        # Test that we clean up rule if we get back to 0 failures
        test_default_check.fails = 1
        test_dryrun_firewall.delRules = AsyncMock()
        test_default_check.run = MagicMock(return_value=0)
        test_dryrun_firewall.rulesExist = AsyncMock(return_value=[69])
        self.loop.run_until_complete(
            rab._ra_block(config, test_dryrun_firewall, test_interface_checks, tp)
        )
        self.assertTrue(test_dryrun_firewall.delRules.called)


if __name__ == "__main__":
    unittest.main()
