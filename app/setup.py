"""Setup script for aging_report package."""
import os

from setuptools import find_packages
from setuptools import setup


setup(
    name="dgs_fiscal",
    version="1.0.0",
    description=("Automates a series of DGS Fiscal workflows"),
    author="Department of General Services",
    author_email="william.daly@baltimorecity.gov",
    install_requires=[
        "dynaconf",
        "O365",
        "pandas",
        "selenium",
        "xlwings",
        "openpyxl",
        "more-itertools",
        "typer",
        "XlsxWriter",
    ],
    include_package_data=True,
    package_dir={"": "src"},  # this is required to access code in src/
    packages=find_packages(where="src"),  # same as above
    entry_points={
        "console_scripts": ["dgs_fiscal=dgs_fiscal:app"],
    },
)
