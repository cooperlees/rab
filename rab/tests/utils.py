#!/usr/bin/env python3

import asyncio
import unittest
from platform import system

from rab.utils import gen_check_output


MACOSX = system() == "Darwin"


class UtilsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_gen_check_output(self) -> None:
        echo_path = "/usr/bin/echo" if MACOSX else "/bin/echo"
        expected = (b"unittest\n", None)
        self.assertEqual(
            expected,
            self.loop.run_until_complete(
                gen_check_output((echo_path, "unittest"), 1)
            ),
        )
