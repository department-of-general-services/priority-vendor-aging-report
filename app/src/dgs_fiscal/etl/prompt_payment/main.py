from __future__ import annotations  # prevents NameError for typehints
from pathlib import Path
from datetime import datetime

import pandas as pd

from dgs_fiscal.systems import CoreIntegrator, SharePoint
from dgs_fiscal.systems.sharepoint import BatchedChanges
from dgs_fiscal.etl.prompt_payment import constants


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

    def get_new_report(self) -> pd.DataFrame:
        """Downloads the most recent Prompt Payment report from CoreIntegrator,
        uploads it to the archive folder, then loads it as a dataframe

        Returns
        -------
        pd.DataFrame
            DataFrame of the new Prompt Payment Report from CoreIntegrator
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
        return df

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

    def reconcile_reports(
        self,
        new_report,
        old_report,
    ) -> BatchedChanges:
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
        pass

    def update_sharepoint(self, changes: BatchedChanges) -> None:
        """Updates sharepoint with the set of changes returned by the
        self.reconcile_reports() method

        Parameters
        ----------
        changes: BatchedChanges
            An instance of BatchedChanges that contains the list changes that
            need to be made to the Invoices list in SharePoint
        """
        pass
