from __future__ import annotations  # prevents NameError for typehints
from typing import List, Dict

import pyodbc
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, aliased
from sqlalchemy.engine import URL
from dynaconf import Dynaconf

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
        self.engine = create_engine(conn_url)
        self._purchase_orders: Records = None
        self._vendors: Records = None
        self._invoices: Records = None

    @property
    def purchase_orders(self):
        """Returns the list of purchase orders"""
        if not self._purchase_orders:
            raise NotImplementedError(
                "The list of Purchase Orders hasn't been queried yet. "
                "Use CitiBuy.get_purchase_orders() to retrieve that list."
            )
        return self._purchase_orders

    @property
    def vendors(self):
        """Returns the list of vendors"""
        if not self._vendors:
            raise NotImplementedError(
                "The list of vendors hasn't been queried yet. "
                "Use CitiBuy.get_vendors() to retrieve that list."
            )
        return self._vendors

    @property
    def invoices(self):
        """Returns the list of vendors"""
        if not self._invoices:
            raise NotImplementedError(
                "The list of invoices hasn't been queried yet. "
                "Use CitiBuy.get_invoices() to retrieve that list."
            )
        return self._vendors

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
        query = select(*po_cols, *ven_cols, *con_cols).limit(limit)
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
