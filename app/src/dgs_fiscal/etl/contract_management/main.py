from __future__ import annotations  # prevents NameError for typehints
from typing import List
from dataclasses import dataclass
from pprint import pprint

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
    po_list: str
        The name of the SharePoint list for Purchase Orders
    vend_list: str
        The name of the SharePoint list for Vendors
    con_list: str
        The name of the SharePoint list for Master Blanket Contracts
    """

    def __init__(
        self,
        citibuy_url: str = None,
        vendor_list: str = "Vendors",
        po_list: str = "Purchase Orders",
        contract_list: str = "Master Blanket POs",
    ) -> None:
        """Inits the ContractManagement class"""
        self.citibuy = CitiBuy(conn_url=citibuy_url)
        self.sharepoint = SharePoint()
        self.po_list = po_list
        self.vendor_list = vendor_list
        self.contract_list = contract_list

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
        con_cols = constants.CITIBUY["contract_cols"]

        # get PO data from citibuy
        df = self.citibuy.get_purchase_orders().dataframe

        # set the PO and Blanket title
        release = df["release_nbr"].astype(str)
        df["po_title"] = np.where(
            release == "0",  # when release number is 0
            "P" + df["po_nbr"],  # drop it from the title: 'P12345'
            "P" + df["po_nbr"] + ":" + release,  # otherwise: 'P12345:1'
        )
        df["contract_title"] = df["po_nbr"] + "- Blanket"

        # sets the PO type
        blanket_po = (release == "0") & (df["start_date"].notna())
        open_market = (release == "0") & (df["start_date"].isna())
        df["po_type"] = "Release"
        df.loc[blanket_po, "po_type"] = "Master Blanket"
        df.loc[open_market, "po_type"] = "Open Market"

        # isloate and format separate dataframes
        df_po = self._get_unique(df, po_cols)
        df_ven = self._get_unique(df, ven_cols)
        df_con = self._get_unique(df, con_cols)

        return ContractData(po=df_po, vendor=df_ven, contract=df_con)

    def get_sharepoint_data(self) -> ContractData:
        """Get current POs and Vendors from their respective SharePoint lists

        Returns
        -------
        ContractData
            A ContractData instance of the PO and vendor data from CitiBuy
        """
        # get the SharePoint list clients
        ven_list = self.sharepoint.get_list(self.vendor_list)
        con_list = self.sharepoint.get_list(self.contract_list)
        po_list = self.sharepoint.get_list(self.po_list)

        # retrieve records from each list
        df_ven = ven_list.get_items().to_dataframe(include_id=True)
        df_con = con_list.get_items().to_dataframe(include_id=True)
        # TODO: Add support for "not in" filter
        po_open = {"Status": ("not equals", "3PCO - Closed")}
        df_po = po_list.get_items(query=po_open).to_dataframe(include_id=True)

        return ContractData(po=df_po, vendor=df_ven, contract=df_con)

    def update_vendor_list(
        self,
        old: pd.Dataframe,
        new: pd.DataFrame,
    ) -> dict:
        """Updates the list of vendors in sharepoint and returns a mapping of
        vendor IDs to SharePoint list item IDs
        """
        ven_list = self.sharepoint.get_list(self.vendor_list)

        # update sharepoint with changes and additions to vendor list
        changes = self._detect_changes(
            old.to_dict("records"),
            new.to_dict("records"),
            key_col="Vendor ID",
        )
        results = ven_list.batch_upsert(changes)

        # build vendor ID mapping for PO lookup
        lookups = dict(zip(old["Vendor ID"], old["id"]))
        for batch in results.inserts:
            for request in batch:
                if request["status"] == 201:
                    ven_id = request["body"]["fields"]["VendorID"]
                    lookups[ven_id] = request["body"]["id"]

        return lookups

    def update_contract_list(
        self,
        old: pd.Dataframe,
        new: pd.DataFrame,
    ) -> dict:
        """Updates the list of contracts in SharePoint and returns a mapping
        of contract PO numbers to SharePoint list item IDs
        """

    def update_po_list(
        self,
        old: pd.Dataframe,
        new: pd.DataFrame,
        vendor_lookup: dict,
    ) -> dict:
        """Updates the list of Purchase Orders in SharePoint and returns
        a mapping of PO and Release numbers to list item IDs
        """
        # replace NaN with None for Open Market POs
        old = old.replace({np.nan: None})
        new = new.replace({np.nan: None})

        # map Vendor ID and PO Number to their lookups
        new["VendorLookupId"] = new["Vendor ID"].map(vendor_lookup)
        # new["ContractLookupId"] = new["PO Number"].map(contract_lookups)
        new = new.drop(columns="Vendor ID")

        # create filter POs that were added and closed in CitiBuy
        added = ~new["Title"].isin(old["Title"])
        closed = ~old["Title"].isin(new["Title"])

        # update POs that were closed since the last run
        closings = pd.Series("3PCO - Closed", old[closed]["id"])
        closings = BatchedChanges(updates=closings.to_dict())
        print("CLOSINGS")
        pprint(closings.updates)

        # add POs that were created since the last run
        created = BatchedChanges(inserts=new[added].to_dict("records"))
        print("PO INSERTS")
        pprint(created.inserts)

        # update POs that already existed in SharePoint
        exists = new[~added].drop(columns="VendorLookupId")
        changes = self._detect_changes(
            old.to_dict("records"),
            exists.to_dict("records"),
            key_col="Title",
        )
        print("PO CHANGES")
        pprint(changes.updates)

    def _get_unique(self, df: pd.DataFrame, cols: dict) -> pd.DataFrame:
        """Isolates and dedupes a subset of the colums from a dataframe"""
        df_new = df[cols.keys()].drop_duplicates()
        df_new.columns = cols.values()
        return df_new

    def _detect_changes(
        self,
        old_items: List[dict],
        new_items: List[dict],
        key_col: str,
    ) -> BatchedChanges:
        """Detects new items that need to be added to SharePoint and existing
        items whose field values have changed and adds them to BatchedChanges

        Parameters
        ----------
        old_items: List[dict]
            List of dictionaries for each existing item in SharePoint
        new_items: List[dict]
            List of dictionaries for each new item from CitiBuy
        key_col: str
            The name of the column that can be used to check if an new item
            already exists in the list of old items
        """
        # init changes and index old_items by key_col
        changes = BatchedChanges()
        old_items = {item[key_col]: item for item in old_items}

        # iterate through new items
        for item in new_items:
            key = item[key_col]
            existing = old_items.pop(key, None)

            # add items that don't already exist to the insert list
            if not existing:
                changes.inserts.append(item)
                continue

            # add items whose values have changed to update list
            for field, new_val in item.items():
                if existing[field] != new_val:
                    changes.updates[existing["id"]] = item
                    break

        return changes


@dataclass
class ContractData:
    """Stores PO and Vendor data as a set of dataframes"""

    po: pd.DataFrame
    vendor: pd.DataFrame
    contract: pd.DataFrame
