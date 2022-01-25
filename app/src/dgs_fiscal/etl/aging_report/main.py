from __future__ import annotations  # prevents NameError for typehints
from typing import Optional

import pandas as pd
from O365.drive import File

from dgs_fiscal.systems import CitiBuy, SharePoint
from dgs_fiscal.etl.aging_report import constants


class AgingReport:
    """Runs the Aging Report workflow, which gets the status of invoices from
    CitiBuy, CoreIntegrator, and Integrify and updates them in SharePoint

    Attributes
    ----------
    citibuy: CitiBuy
        An instance of the CitiBuy class which manages connection to the
        CitiBuy database
    sharepoint: SharePoint
        An instance of the SharePoint class which manages graph API calls to
        SharePoint resources
    """

    def __init__(self, citibuy_url: str) -> None:
        """Inits the AgingReport class"""
        self.citibuy = CitiBuy(conn_url=citibuy_url)
        self.sharepoint = SharePoint()

    def get_citibuy_data(self) -> pd.DataFrame:
        """Gets a list of open and recently paid invoices from CitiBuy so they
        can be uploaded to SharePoint and used to build the AgingReport

        Returns
        -------
        pd.DataFrame
            A dataframe of the invoices exported from CitiBuy
        """
        # query the data from city
        cols = constants.CITIBUY["invoice_cols"]
        df = self.citibuy.get_invoices().dataframe

        # reorder and rename the columns
        df = df[cols.keys()]
        df.columns = cols.values()

        # recode status so it's more descriptive
        df = df.replace(self.citibuy.INVOICE_STATUS)

        return df

    def upload_invoice_data(self, folder_id: Optional[str] = None) -> File:
        """Uploads CitiBuy invoice data to SharePoint as an Excel file

        Parameters
        ----------
        folder_id: str, optional
            The id of the folder to which the invoice data will be uploaded

        Returns
        -------
        File
            Returns an instance of the O365 File class for the Excel file that
            was created in the SharePoint folder passed to this
        """
        pass
