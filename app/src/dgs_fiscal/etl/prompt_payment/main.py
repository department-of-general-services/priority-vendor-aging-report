from __future__ import annotations  # prevents NameError for typehints
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

import pandas as pd
from O365.drive import File

from dgs_fiscal.systems import CoreIntegrator, SharePoint
from dgs_fiscal.etl.prompt_payment import constants, utils

REPORT_PATH = "/Prompt Payment/Prompt Payment Report.xlsx"


@dataclass
class ReportOutput:
    """Output of Prompt Payment Report manipulations"""

    df: pd.DataFrame
    file: Path


class PromptPayment:
    """Runs the Prompt Payment workflow, which scrapes the new Prompt Payment
    report from CoreIntegrator then updates the previous report in SharePoint

    Attributes
    ----------
    core_integrator: CoreIntegrator
        Instance of CoreIntegrator class used to scrape Prompt Payment Report
        from the CoreIntegrator website
    sharepoint: SharePoint
        Instance of SharePoint class used to read and write to the SharePoint
        lists and archive folder associated with the Prompt Payment workflow
    archive: ArchiveFolder
        Instance of ArchiveFolder class that reads from and writes to the
        archive folder in SharePoint
    """

    DGS_LOCATIONS = (
        "DGS - Building Mtce",
        "DGS - CitiBuy",
        "DGS--Fiscal",
        "DGS--Fleet AP",
        "Dept of Gen Serv",
    )

    def __init__(self, local_archive: Path = None) -> None:
        """Inits the PromptPayment class"""
        self.core_integrator = CoreIntegrator()
        self.sharepoint = SharePoint()
        self.archive = self.sharepoint.get_archive_folder(local_archive)

    def get_new_report(self) -> ReportOutput:
        """Downloads the most recent Prompt Payment report from CoreIntegrator,
        uploads it to the archive folder, then loads it as a dataframe

        Returns
        -------
        ReportOutput
            Report output which includes the path to a local copy of the new
            Prompt Payment Report scraped and downloaded from CoreIntegrator
            as well as a dataframe of that report which has been prepared for
            reconciliation with the old report
        """
        dtypes = constants.NEW_REPORT["dtypes"]
        columns = constants.NEW_REPORT["columns"]

        # read scraped report as a dataframe
        file = self.core_integrator.scrape_report()
        df = pd.read_excel(file, dtype=dtypes, engine="openpyxl")

        # zfill vendor_id to 8 characters
        df["Vendor ID"] = df["Vendor ID"].str.zfill(8)

        # filter for invoices in DGS employee queue
        dgs_location = df["Location"].isin(self.DGS_LOCATIONS)
        dgs_status = df["Status"] == "Awaiting Agency Contact"
        df = df[dgs_location & dgs_status].copy()

        # calculate date invoice was assigned to DGS
        today = pd.Series(datetime.today(), df.index)
        status_age = pd.to_timedelta(df["Status Age (days)"], unit="D")
        df["Assigned Date (Core)"] = today - status_age

        # convert Julian Excel date to datetime
        julian = df["Creation Date"] + 2415018
        julian = pd.to_datetime(julian, unit="D", origin="julian")
        df["Creation Date"] = julian.dt.date.astype("datetime64")

        # TODO: matches DGS staff names to O365 profile

        # preserve and rename a subset of columns for matching
        df = df[columns.keys()]
        df.columns = columns.values()

        return ReportOutput(df=df, file=file)

    def get_old_report(self) -> pd.DataFrame:
        """Retrieves the previous Prompt Payment report from SharePoint,
        uploads it to the archive, then loads it as a DataFrame

        Returns
        -------
        pd.DataFrame
            A dataframe of the old Prompt Payment report pulled from SharePoint
        """
        invoice_list = self.sharepoint.get_list("Invoices")

        query = {"Prompt Payment": ("equals", 1)}
        invoices = invoice_list.get_items(query=query)
        return invoices.to_dataframe()

    def get_old_excel(
        self,
        report_path: Optional[str] = REPORT_PATH,
        download_loc: Optional[Path] = None,
    ) -> pd.DataFrame:
        """Retrieves the previous Prompt Payment report from SharePoint

        This method is different from get_old_report() because it pulls the
        report from the Excel file instead of the SharePoint list

        Returns
        -------
        ReportOutput
            Report output which includes the path to a local copy of the old
            Prompt Payment Report downloaded from SharePoint as well as a
            dataframe of that report which has been prepared for reconciliation
            with the new report from CoreIntegrator
        """
        # get the list of columns and dtypes
        dtypes = constants.OLD_REPORT["dtypes"]
        print(dtypes)

        # Set the download location
        download_loc = download_loc or Path.cwd() / "archives"
        file = self.sharepoint.get_item_by_path(report_path)
        tmp_file = download_loc / file.name

        # download and read in file from SharePoint
        file.download(download_loc)
        df = pd.read_excel(tmp_file, dtype=dtypes)

        # zfill vendor_id to 8 characters
        df["Vendor ID"] = df["Vendor ID"].str.zfill(8)

        # preserve only a subset of columns for matching
        df = df[dtypes.keys()]

        return ReportOutput(df=df, file=tmp_file)

    def reconcile_reports(
        self,
        new_report: pd.DataFrame,
        old_report: pd.DataFrame,
        export_path: Optional[Path] = None,
    ) -> ReportOutput:
        """Merges the old report from SharePoint with the new report scraped
        from CoreIntegrator and return a list of the changes to make

        Parameters
        ----------
        new_report: pd.DataFrame
            A DataFrame of the new Prompt Payment report that was scraped from
            CoreIntegrator
        old_report: pd.DataFrame
            A DataFrame of the records added or updated in SharePoint in the
            previous run of the Prompt Payment report

        Returns
        -------
        ReportOutput
            An instance of ReportOutput with the reconciled report as both a
            dataframe and a locally saved and formatted file
        """
        df = self._merge_reports(new_report, old_report)
        file = self._export_report(df=df, export_path=export_path)
        return ReportOutput(df=df, file=file)

    def update_sharepoint(
        self,
        file_path: Path,
        report_name: str,
        folder_name: str,
    ) -> File:
        """Uploads CitiBuy invoice data to SharePoint as an Excel file

        Parameters
        ----------
        file_path: Path
            Path to the local file to upload
        folder_name: str, optional
            The name of the folder to which the invoice data will be uploaded

        Returns
        -------
        File
            Returns an instance of the O365 File class for the Excel file that
            was uploaded to SharePoint
        """
        # set the file name to the current date
        date_str = datetime.today().strftime("%Y-%m-%d")
        file_name = f"{date_str}_{report_name}.xlsx"

        # upload the exported file to SharePoint
        return self.archive.upload_file(file_path, folder_name, file_name)

    def _merge_reports(
        self,
        new_report: pd.DataFrame,
        old_report: pd.DataFrame,
    ) -> pd.DataFrame:
        """Merges the old report from SharePoint with the new report scraped
        from CoreIntegrator and return a list of the changes to make

        Parameters
        ----------
        new_report: pd.DataFrame
            A DataFrame of the new Prompt Payment report that was scraped from
            CoreIntegrator
        old_report: pd.DataFrame
            A DataFrame of the records added or updated in SharePoint in the
            previous run of the Prompt Payment report

        Returns
        -------
        BatchedChanges

        """
        # merge reports on vendor_id and document_number
        # preserve all of the rows in Core Integrator report
        merge_fields = ["Vendor ID", "Document Number"]
        for field in merge_fields:
            assert field in new_report.columns
            assert field in old_report.columns
        df = new_report.merge(old_report, how="left", on=merge_fields)
        print(df.columns)

        # compute additional fields and sort dataframe
        df["Age of Invoice"] = utils.compute_age_of_invoice(df)
        df["Days Outstanding"] = utils.compute_days_outstanding(df)
        df["Days with BAPS"] = utils.compute_days_with_baps(df)
        df = utils.update_division(df)

        # return reconciled report with oldest invoices listed first
        return df.sort_values(by="Age of Invoice", ascending=False)

    def _export_report(
        self,
        df: pd.DataFrame,
        export_path: Optional[Path] = None,
        sheet_name: str = "Prompt Payment",
    ) -> Path:
        """Saves a copy of the report in the 'archives/output/' directory
        Args:
            df (dataframe): Merged report that will be archived
            dir (path): Location where the archived report will be saved
            src_file (path): Location of file to read validation data from
            src_sheet (string): Name of the sheet with validation data
        Returns:
            file (path): Location of archived file
        """
        # set export directory to local archive
        dir = export_path or self.archive.tmp_dir

        # get current date
        today = datetime.today()
        format = "%Y-%m-%d"
        date_str = datetime.strftime(today, format)

        # set path for copied file
        file = dir / f"joint_report{date_str}.xlsx"

        # export dataframe and format
        with pd.ExcelWriter(
            file, engine="openpyxl", datetime_format="MM/DD/YYYY"
        ) as writer:
            # write
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            # update formatting and save
            wb = writer.book
            utils.format_workbook(wb)
            writer.save()

        return file
