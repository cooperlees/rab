#!/usr/bin/env python3

import argparse
import logging
import sys


LOG = logging.getLogger(__name__)


def _handle_logging(debug: bool) -> None:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    _handle_logging(args.debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
