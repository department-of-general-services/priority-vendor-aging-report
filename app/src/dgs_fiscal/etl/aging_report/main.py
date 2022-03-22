from __future__ import annotations  # prevents NameError for typehints
from typing import Optional
from pathlib import Path
from datetime import datetime

import pandas as pd
from O365.drive import File

from dgs_fiscal.systems import CitiBuy, SharePoint
from dgs_fiscal.etl.aging_report import constants

REPORT_PATH = "/Prompt Payment/Priority Vendor (Aging) Report/AgingReport.xlsx"


class AgingReport:
    """Manages execution of the Aging Report workflow

    The aging Aging Report workflow aggregates the status of invoices from
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

    def __init__(self, citibuy_url: str = None) -> None:
        """Inits the AgingReport class"""
        self.citibuy = CitiBuy(conn_url=citibuy_url)
        self.sharepoint = SharePoint()

    def get_sharepoint_data(
        self,
        report_path: Optional[str] = REPORT_PATH,
        download_loc: Optional[Path] = None,
    ) -> pd.DataFrame:
        """Retrieves blank aging report from SharePoint

        Parameters
        ----------
        folder_path: str, optional
            Path to the folder
        """
        # Set the download location
        download_loc = download_loc or Path.cwd() / "archives"
        file = self.sharepoint.get_item_by_path(report_path)
        tmp_file = download_loc / file.name

        # download and read in file from SharePoint
        file.download(download_loc)
        return pd.read_excel(tmp_file, dtype={"Vendor ID": "string"})

    def get_citibuy_data(self, invoice_window: int = 365) -> pd.DataFrame:
        """Exports open and recently paid invoices from CitiBuy

        Parameters
        ----------
        invoice_window: int
            The maximum number of days in the past an invoice must have been
            paid or cancelled in order to be included in the exported results

        Returns
        -------
        pd.DataFrame
            A dataframe of the invoices exported from CitiBuy
        """
        # query the data from city,
        # including invoices paid or cancelled up to a year ago
        df = self.citibuy.get_invoices(days_ago=invoice_window).dataframe

        # add PO type column
        open_market = df["contract_end_date"].isna()
        df["po_type"] = "Release"
        df.loc[open_market, "po_type"] = "Open Market"

        # reorder and rename the columns
        cols = constants.CITIBUY["invoice_cols"]
        df = df[cols.keys()]
        df.columns = cols.values()

        # recode invoice and PO statuses so they're more descriptive
        df = df.replace(self.citibuy.INVOICE_STATUS)
        df = df.replace(self.citibuy.PO_STATUS)

        return df

    def upload_invoice_data(
        self,
        df: pd.DataFrame,
        folder_name: Optional[str] = None,
        local_archive: Optional[Path] = None,
    ) -> File:
        """Uploads CitiBuy invoice data to SharePoint as an Excel file

        Parameters
        ----------
        df: pd.DataFrame
            A dataframe of the invoice data to upload to SharePoint
        folder_name: str, optional
            The name of the folder to which the invoice data will be uploaded
        local_archive: Path, optional
            Path to local directory where export will be saved before being
            uploaded to SharePoint. Default is archives/ directory at root.

        Returns
        -------
        File
            Returns an instance of the O365 File class for the Excel file that
            was uploaded to SharePoint
        """
        # set the file name to the current date
        date_str = datetime.today().strftime("%Y-%m-%d")
        file_name = f"{date_str}_InvoiceExport.xlsx"

        # export the invoice data to local archive
        archive = self.sharepoint.get_archive_folder(local_archive)
        tmp_file = archive.export_dataframe(df, file_name)

        # upload the exported file to SharePoint
        folder = folder_name or "aging_report"
        print(folder)
        return archive.upload_file(tmp_file, folder, file_name)
