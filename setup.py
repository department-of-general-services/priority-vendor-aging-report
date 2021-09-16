"""Setup script for aging_report package."""
import os

from setuptools import find_packages
from setuptools import setup


setup(
    name="aging_report",
    version="1.0.0",
    description=(
        "Automates the process for updating the Priority Vendor Aging Report",
    ),
    author="Department of General Services",
    author_email="william.daly@baltimorecity.gov",
    install_requires=[
        "dynaconf",
        "O365",
        "pandas",
        "selenium",
        "xlwings",
        "openpyxl",
    ],
    include_package_data=True,
    package_dir={"": "src"},  # this is required to access code in src/
    packages=find_packages(where="src"),  # same as above
)
