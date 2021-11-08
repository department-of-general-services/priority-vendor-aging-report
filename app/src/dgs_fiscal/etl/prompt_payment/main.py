from __future__ import annotations  # prevents NameError for typehints
from pathlib import Path

import pandas as pd

from dgs_fiscal.systems import CoreIntegrator, SharePoint
from dgs_fiscal.systems.sharepoint import BatchedChanges


class PromptPayment:
    """Manages access to the Prompt Payment Report in CoreIntegrator, which
    serves as a data source for updates to the Aging Report in SharePoint

    Attributes
    ----------
    core_integrator: CoreIntegrator
        Instance of CoreIntegrator class used to scrape Prompt Payment Report
        from the CoreIntegrator website
    sharepoint: SharePoint
        Instance of SharePoint class used to read and write to the SharePoint
        lists and archive folder associated with the Prompt Payment workflow
    """

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
            DataFrame of the Prompt Payment Report from CoreIntegrator
        """
        return self.core_integrator.scrape_report()

    def get_old_report(self) -> pd.DataFrame:
        """Retrieves the previous Prompt Payment report from SharePoint,
        uploads it to the archive, then loads it as a DataFrame

        Returns
        -------
        pd.DataFrame
            A dataframe of the Prompt Payment report pulled from SharePoint
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
        from CoreIntegrator and return a list of the changes

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
