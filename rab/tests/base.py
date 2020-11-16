#!/usr/bin/env python3

import unittest

from rab.tests.firewalls import NftablesTests  # noqa: F401
from rab.tests.utils import UtilsTests  # noqa: F401

import rab


class BaseTests(unittest.TestCase):
    def test_handle_logging(self) -> None:
        self.assertIsNone(rab._handle_logging(False))

    def test_parse_args(self) -> None:
        self.assertTrue(rab._parse_args())

    def test_read_config(self) -> None:
        self.assertEqual({}, rab._read_config("/tmp/not_there.json"))


if __name__ == "__main__":
    unittest.main()
