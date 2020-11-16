#!/usr/bin/env python3

import asyncio
import unittest
from unittest.mock import AsyncMock

from rab.firewalls import NftablesCLI
from rab.tests.fixtures import NFTABLES_TABLE_JSON_NO_RULE, NFTABLES_TABLE_JSON_ONE_RULE


class NftablesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.nft = NftablesCLI()

    def test_rulesExist(self) -> None:
        tests = (
            ([], AsyncMock(return_value=NFTABLES_TABLE_JSON_NO_RULE)),
            ([17], AsyncMock(return_value=NFTABLES_TABLE_JSON_ONE_RULE)),
        )
        for expected, mock in tests:
            self.nft.listRules = mock
            found_rules = self.loop.run_until_complete(self.nft.rulesExist())
            self.assertEqual(expected, found_rules)
