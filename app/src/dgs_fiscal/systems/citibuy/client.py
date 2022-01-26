from __future__ import annotations  # prevents NameError for typehints
from typing import List
from datetime import date, timedelta

import pyodbc
import sqlalchemy as sa
from sqlalchemy.orm import Session, aliased
from sqlalchemy.engine import URL, Row
from dynaconf import Dynaconf
import pandas as pd

from dgs_fiscal.config import settings
from dgs_fiscal.systems.citibuy import models


class CitiBuy:
    """Client that interfaces with the CitiBuy backend

    Attributes
    ----------
    engine: sqlalchemy.Engine
    """

    INVOICE_STATUS = {
        "4II": "4II - In Progress",
        "4IR": "4IR - Ready for Approval",
        "4IA": "4IA - Approved for Payment",
        "4IP": "4IP - Paid",
        "4IC": "4IC - Cancelled",
        "4IRT": "4IRT - Returned",
    }
    PO_STATUS = {
        "3PRS": "3PRS - Ready to Send",
        "3PS": "3PS - Sent",
        "3PRT": "3PRT - Returned",
        "3PRA": "3PRA - Ready for Approval",
        "3PPR": "3PPR - Partial Receipt",
        "3PI": "3PI - In Progress",
        "3PCR": "3PCR - Completed Receipt",
        "3PCO": "3PCO - Closed",
    }

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
        self.engine = sa.create_engine(conn_url)

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
                query = sa.text(query_str)
                rows = conn.execute(query).fetchall()
        except sa.exc.ProgrammingError as error:
            raise error
        return DatabaseRows(rows)

    def get_purchase_orders(  # pylint: disable=too-many-locals
        self,
        limit: int = 10000,
    ) -> DatabaseRows:
        """Gets a list of POs from CitiBuy and returns them as a list of dicts

        Parameters
        ----------
        limit: int
            Number of records to return from the query results

        Returns
        -------
        DatabaseRows
            An instance of DatabaseRows for the purchase order records
        """
        # create aliases for the tables
        po = aliased(models.PurchaseOrder, name="po")
        ven = aliased(models.Vendor, name="v")
        con = aliased(models.BlanketContract, name="c")
        addr = aliased(models.Address, name="a")
        va = aliased(models.VendorAddress, name="va")

        # extract the columns to include in the query
        query = sa.select(
            *[getattr(po, col) for col in po.columns],  # PO columns
            *[getattr(ven, col) for col in ven.columns],  # Vendor cols
            *[getattr(con, col) for col in con.columns],  # Contract cols
            *[getattr(addr, col) for col in addr.columns],  # Address cols
        ).limit(limit)

        # join the contract, vendor, and address tables
        dgs_contract = con.contract_agency.in_(("AGY", "DGS"))
        fkey_contract = (dgs_contract) & (po.po_nbr == con.po_nbr)
        fkey_vendor = po.vendor_id == ven.vendor_id
        fkey_address = addr.address_id == va.address_id
        fkey_va = (
            (va.vendor_id == ven.vendor_id)
            & (va.address_type == "M")
            & (va.default == "Y")
        )
        query = query.join(po, fkey_vendor)
        query = query.join(con, fkey_contract, isouter=True)
        query = query.join(va, fkey_va, isouter=True)
        query = query.join(addr, fkey_address, isouter=True)

        # filter for recent blanket contracts and open market POs
        open_market = con.contract_agency.is_(None)
        not_closed = con.end_date > (date.today() - timedelta(90))
        query = query.where(open_market | not_closed)

        # filter for DGS releases or blanket POs available to DGS
        dgs_release = po.agency == "DGS"
        blanket_po = po.release_nbr == 0
        query = query.where(dgs_release | (blanket_po & dgs_contract))

        # filter out POs and releases that are closed
        query = query.where(po.status.notin_(("3PCO", "3PCA")))

        with Session(self.engine) as session:
            rows = session.execute(query).fetchall()
        return DatabaseRows(rows)

    def get_invoices(self) -> DatabaseRows:
        """Gets a list of invoices from CitiBuy and returns them as a list
        of dictionaries

        Returns
        -------
        DatabaseRows
            An instance of DatabaseRows for the invoice records
        """
        # create aliases for the tables
        po = aliased(models.PurchaseOrder, name="po")
        ven = aliased(models.Vendor, name="vendor")
        inv = aliased(models.Invoice, name="invoice")
        # status = aliased(models.InvoiceStatusHistory, name="status")

        # create the foreign keys
        # fkey_status = inv.id == status.invoice_id
        fkey_vendor = inv.vendor_id == ven.vendor_id
        fkey_po = (po.po_nbr == inv.po_nbr) & (
            po.release_nbr == inv.release_nbr
        )

        # TODO: remove this section
        # create a sub-query for recently closed and cancelled invoices
        # updated_recently = status.status_date > (date.today() - timedelta(45))
        # closed = sa.select(inv.id)
        # closed = closed.join(status, fkey_status)
        # closed = closed.where(inv.status == status.to_status)
        # closed = closed.where(updated_recently)
        # closed = closed.cte("recently_closed")  # creates a WITH clause
        # closed = sa.select(closed.c.id)  # isloates invoice ids from clause

        # create the return query
        query = sa.select(
            # invoice columns and vendor name
            ven.name,
            *[getattr(inv, col) for col in inv.columns],
        )
        query = query.join(ven, fkey_vendor)
        query = query.join(po, fkey_po)
        query = query.where(po.agency == "DGS")  # invoice created from DGS PO
        query = query.where(
            # invoice still open or recently closed or cancelled
            (inv.status.not_in(("4IP", "4IC")))
            | (inv.modified > (date.today() - timedelta(45)))
        )
        with Session(self.engine) as session:
            rows = session.execute(query).fetchall()
        return DatabaseRows(rows)


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
