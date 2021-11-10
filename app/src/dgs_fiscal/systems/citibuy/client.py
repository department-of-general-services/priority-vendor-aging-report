from __future__ import annotations  # prevents NameError for typehints
from typing import List, Dict

import pyodbc
import sqlalchemy
from sqlalchemy.orm import Session, aliased
from sqlalchemy.engine import URL, Row
from dynaconf import Dynaconf
import pandas as pd

from dgs_fiscal.config import settings
from dgs_fiscal.systems.citibuy import models

Records = List[dict]


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
        self._purchase_orders: Records = None

    @property
    def purchase_orders(self):
        """Returns the list of purchase orders"""
        if not self._purchase_orders:
            raise NotImplementedError(
                "The list of Purchase Orders hasn't been queried yet. "
                "Use CitiBuy.get_purchase_orders() to retrieve that list."
            )
        return self._purchase_orders

    def execute_stmt(self, query_str: str) -> DatabaseRows:
        """Executes a SQL query against the CitiBuy database

        Parameters
        ----------
        query_str: str
            A string with valid SQL syntax
        fetch: FetchOpts
            How many rows should be fetched from the cursor, either all or
            just the first. Default is to return all.

        Returns
        -------
        DatabaseRows
            An instance of DatabaseRows with the results from the query
        """
        try:
            with self.engine.connect() as conn:
                query = sqlalchemy.text(query_str)
                rows = conn.execute(query).fetchall()
        except sqlalchemy.exc.ProgrammingError as error:
            raise error
        return DatabaseRows(rows)

    def _rows_to_dicts(self, cursor):
        """Converts SQLAlchemy rows to a list of dicts keyed by column name"""
        return [row._asdict() for row in cursor.all()]

    def get_purchase_orders(self, limit: int = 100) -> Records:
        """Gets a list of POs from CitiBuy and returns them as a list of dicts

        Parameters
        ----------
        limit: int
            Number of records to return from the query results

        Returns
        -------
        Records
            A list of results as a dictionary keyed by the column names
        """
        # create aliases for the tables
        po = aliased(models.PurchaseOrder, name="po")
        ven = aliased(models.Vendor, name="v")
        con = aliased(models.BlanketContract, name="c")

        # extract the columns to include in the query
        po_cols = [getattr(po, col) for col in po.columns]
        ven_cols = [getattr(ven, col) for col in ven.columns]
        con_cols = [getattr(con, col) for col in con.columns]

        # build the base query
        query = sqlalchemy.select(*po_cols, *ven_cols, *con_cols).limit(limit)
        query = query.join(po, po.vendor_id == ven.id)
        query = query.join(
            con,
            (po.po_nbr == con.po_nbr) & (po.release_nbr == con.release_nbr),
            isouter=True,
        )
        query = query.where(po.agency.in_(("DGS", "AGY")))

        with Session(self.engine) as session:
            cursor = session.execute(query)
            self._purchase_orders = self._rows_to_dicts(cursor)
        return self.purchase_orders

    def get_invoices(
        self,
        limit: int = 100,
        filter_dict: Dict[str, tuple] = None,
    ) -> Records:
        """Gets a list of Invoices from CitiBuy and returns them as a list
        of dictionaries

        Parameters
        ----------
        limit: int
            Number of records to return from the query results
        filter_dict: Dict[str, tuple]
            Conditions applied to fields on the PO used to filter the results.
            Must be passed in this format: {"col_name": ("equals", "dog")}

        Returns
        -------
        Records
            A list of results as a dictionary keyed by the column names
        """
        pass


class DatabaseRows:
    """A class that provides simplified access to the results of a SQL query

    Attributes
    ----------
    rows: List[Row]
        A list of SQLAlchemy Row instances that are returned by a query
    row_type: str
        The type of values included in each row, "columns" indicates that each
        row is a named tuple of the columns returned from a query, while "orm"
        indicates that each row is a named tuple of the orm models returned.
    cols: tuple
        A tuple of the names of the columns returned by the query
    """

    def __init__(self, rows: List[Row], row_type: str = "columns") -> None:
        """Inits the DatabaseRows class"""
        self.rows = rows
        self.row_type = row_type
        self.cols = rows[0]._fields

    @property
    def dataframe(self) -> pd.DataFrame:
        """Returns the rows as a pandas dataframe"""
        return pd.DataFrame(self.rows, columns=self.cols)

    @property
    def records(self) -> List[dict]:
        """Returns the rows as a list of dictionaries"""
        return [row._asdict() for row in self.rows]
