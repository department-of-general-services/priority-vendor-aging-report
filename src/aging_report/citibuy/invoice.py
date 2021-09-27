from __future__ import annotations  # prevents NameError for typehints
from typing import List, Dict

from aging_report.citibuy.client import CitiBuy


class Invoice(CitiBuy):
    """Client that organizes queries of Invoice data from CitiBuy"""

    def __init__(self) -> None:
        """Instantiates the Invoice class"""
        pass

    def get_invoices(
        self,
        limit: int = 100,
        filter_dict: Dict[str, tuple] = None,
    ) -> List[dict]:
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
        List[dict]
            A list of results as a dictionary keyed by the column names
        """
        pass

    def update_invoice_list(self) -> None:
        """Updates the Invoice SharePoint list with data from CitiBuy"""
        pass
