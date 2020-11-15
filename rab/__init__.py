#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any


LOG = logging.getLogger(__name__)


def _handle_logging(debug: bool) -> None:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-c", "--config", default="/config/rab.json", help="Path of JSON config file"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    return parser.parse_args()


def _read_config(path_str: str) -> Any:
    config_path = Path(path_str)

    if not config_path.exists():
        LOG.error(f"{config_path} does not exist.")
        return {}

    with config_path.open("r") as cfp:
        return json.load(cfp)


def main() -> int:
    args = _parse_args()
    _handle_logging(args.debug)

    config_dict = _read_config(args.config)
    if not config_dict:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
