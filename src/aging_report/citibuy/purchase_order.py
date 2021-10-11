from __future__ import annotations  # prevents NameError for typehints
from typing import List

from dynaconf import Dynaconf
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from aging_report.config import settings
from aging_report.citibuy import models, CitiBuy
from aging_report.sharepoint import SharePoint

# gets list of columns for each model
VENDOR_COLS = ("name", "contact", "email", "phone")
PO_COLS = (
    "po_nbr",
    "release_nbr",
    "agency",
    "status",
    "date",
    "cost",
    "vendor_id",
)
CONTRACT_COLS = (
    "contract_agency",
    "start_date",
    "end_date",
    "dollar_limit",
    "dollar_spent",
)


class PurchaseOrders(CitiBuy):
    """Client that organizes queries of Purchase Order data from CitiBuy"""

    def __init__(
        self,
        config: Dynaconf = settings,
        conn_url: str = None,
    ) -> None:
        """Instantiates the Purchase Order class"""
        print(conn_url)
        super().__init__(config, conn_url)
        self.sharepoint: SharePoint = None  # not instantiated until needed
        self._records: List[dict] = None

    @property
    def records(self) -> List[dict]:
        """Returns the list of records retrieved by self.get_records()"""
        # raise an error if self.get_records() hasn't been called
        if not self._records:
            raise AttributeError(
                "No records have been retrieved from the database yet, "
                "use get_records() to populate the records attribute"
            )
        return self._records

    def get_records(
        self,
        limit: int = 100,
    ) -> List[dict]:
        """Gets a list of POs from CitiBuy and returns them as a list of dicts

        Parameters
        ----------
        limit: int
            Number of records to return from the query results
        filter_dict: Dict[str, tuple]
            Conditions applied to fields on the PO used to filter the results.
            Must be passed in this format: {"col_name": ("equals", "dog")}

        Returns
        -------
        List[dict]
            A list of results as a dictionary keyed by the column names
        """
        # create aliases for the tables
        po = aliased(models.PurchaseOrder, name="po")
        ven = aliased(models.Vendor, name="v")
        con = aliased(models.BlanketContract, name="c")

        # extract the columns to include in the query
        po_cols = [getattr(po, col) for col in PO_COLS]
        ven_cols = [getattr(ven, col) for col in VENDOR_COLS]
        con_cols = [getattr(con, col) for col in CONTRACT_COLS]

        # build the base query
        query = select(*po_cols, *ven_cols, *con_cols).limit(limit)
        query = query.join(po, po.vendor_id == ven.id)
        query = query.join(
            con,
            (po.po_nbr == con.po_nbr) & (po.release_nbr == con.release_nbr),
            isouter=True,
        )
        query = query.where(po.agency.in_(("DGS", "AGY")))

        print(query)
        with Session(self.engine) as session:
            cursor = session.execute(query)
            return super().rows_to_dicts(cursor)

    def update_po_list(self) -> None:
        """Updates the Purchase Order SharePoint list with data from CitiBuy"""
        pass

    def update_vendor_list(self) -> None:
        """Updates the Vendor SharePoint list with data from CitiBuy"""
        pass
