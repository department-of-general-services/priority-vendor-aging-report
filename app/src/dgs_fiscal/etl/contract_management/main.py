from __future__ import annotations  # prevents NameError for typehints
from typing import List
from dataclasses import dataclass

import pandas as pd
import numpy as np

from dgs_fiscal.systems import CitiBuy, SharePoint
from dgs_fiscal.systems.sharepoint import BatchedChanges
from dgs_fiscal.etl.contract_management import constants


class ContractManagement:
    """Runs the Contract Management workflow, which gets the list of active
    Purchase Orders and vendors from CitiBuy and adds them to SharePoint

    Attributes
    ----------
    citibuy: CitiBuy
        An instance of the CitiBuy class which connects to and queries data
        from the CitiBuy database
    sharepoint: SharePoint
        Instance of SharePoint class used to read and write to the SharePoint
        lists and folders associated with the Contract Management workflow
    """

    def __init__(self, citibuy_url: str = None) -> None:
        """Inits the ContractManagement class"""
        self.citibuy = CitiBuy(conn_url=citibuy_url)
        self.sharepoint = SharePoint()

    def get_citibuy_data(self) -> ContractData:
        """Gets the list of active or recently closed Purchase Orders and the
        unique list of DGS vendors from CitiBuy

        Returns
        -------
        ContractData
            A ContractData instance of the PO and vendor data from CitiBuy
        """
        po_cols = constants.CITIBUY["po_cols"]
        ven_cols = constants.CITIBUY["vendor_cols"]

        # get PO data from citibuy
        df = self.citibuy.get_purchase_orders().dataframe

        # set the PO title
        release = df["release_nbr"].astype(str)
        df["po_title"] = np.where(
            release == "0",  # when release number is 0
            "P" + df["po_nbr"],  # drop it from the title: 'P12345'
            "P" + df["po_nbr"] + ":" + release,  # otherwise: 'P12345:1'
        )

        # isloate and format PO dataframe
        df_po = df[po_cols.keys()]
        df_po.columns = po_cols.values()

        # isolate and format Vendor dataframe
        df_ven = df[ven_cols.keys()]
        df_ven = df_ven.drop_duplicates()
        df_ven.columns = ven_cols.values()

        return ContractData(po=df_po, vendor=df_ven)

    def get_sharepoint_data(self, dataset: str) -> List[dict]:
        """Get current POs and Vendors from their respective SharePoint lists"""
        pass

    def reconcile_lists(
        self,
        citibuy_data: List[dict],
        sharepoint_data: List[dict],
    ) -> BatchedChanges:
        """Compares the lists of POs and vendors pulled from CitiBuy with the
        data currently in SharePoint and returns a list of the changes to make

        Parameters
        ----------
        citibuy_data: List[dict]
            A DataFrame of the new Prompt Payment report that was scraped from
            CoreIntegrator
        sharepoint_data: List[dict]
            A DataFrame of the records added or updated in SharePoint in the
            previous run of the Prompt Payment report
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


@dataclass
class ContractData:
    """Stores PO and Vendor data as a set of dataframes"""

    po: pd.DataFrame
    vendor: pd.DataFrame
