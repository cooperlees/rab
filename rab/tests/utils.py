#!/usr/bin/env python3

import asyncio
import unittest

from rab.utils import gen_check_output


class UtilsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_gen_check_output(self) -> None:
        expected = (b"unittest\n", None)
        self.assertEqual(
            expected,
            self.loop.run_until_complete(
                gen_check_output(("/usr/bin/echo", "unittest"), 1)
            ),
        )
