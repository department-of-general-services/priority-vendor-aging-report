from __future__ import annotations  # prevents NameError for typehints
from typing import List

from dynaconf import Dynaconf

from aging_report.config import settings


class CitiBuy:
    """Client that interfaces with the CitiBuy backend"""

    def __init__(self, config: Dynaconf = settings) -> None:
        """Instantiates the CitiBuy class"""
        pass

    def query_many(self, query_str) -> List[dict]:
        """Executes a query and returns the results as a list of dicts"""
        pass
