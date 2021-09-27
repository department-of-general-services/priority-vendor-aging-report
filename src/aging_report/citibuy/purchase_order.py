from __future__ import annotations  # prevents NameError for typehints
from typing import List, Dict

from aging_report.citibuy.client import CitiBuy
from aging_report.sharepoint import Client, ArchiveFolder


class PurchaseOrder(CitiBuy):
    """Client that organizes queries of Purchase Order data from CitiBuy"""

    def __init__(self) -> None:
        """Instantiates the Purchase Order class"""
        pass

    def get_purchas_orders(
        self,
        limit: int = 100,
        filter_dict: Dict[str, tuple] = None,
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
        pass

    def update_po_list(self) -> None:
        """Updates the Purchase Order SharePoint list with data from CitiBuy"""
        pass

    def update_vendor_list(self) -> None:
        """Updates the Vendor SharePoint list with data from CitiBuy"""
        pass
