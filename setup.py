#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup


ptr_params = {
    "entry_point_module": "rab",
    "test_suite": "rab.tests.base",
    "test_suite_timeout": 10,
    "required_coverage": {"rab/__init__.py": 1},
    "run_black": True,
    "run_mypy": False,  # enable once we have code :D
    "run_flake8": True,
}


def get_long_desc() -> str:
    repo_base = Path(__file__).parent
    long_desc = ""
    for info_file in (repo_base / "README.md", repo_base / "CHANGES.md"):
        with info_file.open("r", encoding="utf8") as ifp:
            long_desc += ifp.read()
        long_desc += "\n\n"

    return long_desc


setup(
    name=ptr_params["entry_point_module"],
    version="20.11.14",
    description="RA Blocker stops RAs while your WAN is down",
    long_description=get_long_desc(),
    long_description_content_type="text/markdown",
    py_modules=["rab", "rab.tests"],
    url="http://github.com/cooperlees/rab",
    author="Cooper Lees",
    author_email="me@cooperlees.com",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=["pyroute2"],
    entry_points={"console_scripts": ["rab = rab:__init__"]},
    test_suite=ptr_params["test_suite"],
)
