#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup


ptr_params = {
    "entry_point_module": "rab/__init__",
    "test_suite": "rab.tests.base",
    "test_suite_timeout": 10,
    "required_coverage": {
        "rab/__init__.py": 70,
        "rab/firewalls.py": 40,
        "rab/utils.py": 65,
        "TOTAL": 50,
    },
    "run_black": True,
    "run_mypy": True,
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
    name="rab",
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
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=["pyroute2"],
    entry_points={"console_scripts": ["rab = rab:main"]},
    test_suite=ptr_params["test_suite"],
)
