from __future__ import annotations  # prevents NameError for typehints
from typing import List

import pyodbc
import sqlalchemy
from sqlalchemy.engine import URL
from sqlalchemy import text
from dynaconf import Dynaconf

from aging_report.config import settings


class CitiBuy:
    """Client that interfaces with the CitiBuy backend

    Attributes
    ----------
    engine: sqlalchemy.Engine
    """

    def __init__(
        self,
        config: Dynaconf = settings,
        conn_url: str = None,
    ) -> None:
        """Instantiates the CitiBuy class and connects to the database"""
        if not conn_url:
            conn_str = (
                "Driver={SQL Server};"
                f"Server={config.citibuy_server};"
                f"Database={config.citibuy_db};"
                f"UID={config.citibuy_username};"
                f"PWD={config.citibuy_password};"
            )
            pyodbc.pool = False
            conn_url = URL.create(
                "mssql+pyodbc", query={"odbc_connect": conn_str}
            )
        self.engine = sqlalchemy.create_engine(conn_url)

    def query(self, query_str: str) -> List[dict]:
        """Executes a query and returns the results as a list of dicts

        Parameters
        ----------
        query_str: str
            A string with valid SQL syntax
        fetch: FetchOpts
            How many rows should be fetched from the cursor, either all or
            just the first. Default is to return all.

        Returns
        -------
        List[dict]
            List of records as dictionaries keyed by column name
        """
        exceptions = (
            sqlalchemy.exc.ProgrammingError,
            sqlalchemy.exc.OperationalError,
        )
        try:
            with self.engine.connect() as conn:
                query = text(query_str)
                cursor = conn.execute(query)
                return self.rows_to_dicts(cursor)
        except exceptions as error:
            raise error

    def rows_to_dicts(self, cursor):
        """Converts SQLAlchemy rows to a list of dicts keyed by column name"""
        return [row._asdict() for row in cursor.all()]
