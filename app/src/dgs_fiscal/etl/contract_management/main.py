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

        # sets the PO type
        blanket_po = (release == "0") & (df["start_date"].notna())
        open_market = (release == "0") & (df["start_date"].isna())
        df["po_type"] = "Release"
        df.loc[blanket_po, "po_type"] = "Master Blanket"
        df.loc[open_market, "po_type"] = "Open Market"

        # isloate and format PO dataframe
        df_po = df[po_cols.keys()]
        df_po.columns = po_cols.values()

        # isolate and format Vendor dataframe
        df_ven = df[ven_cols.keys()]
        df_ven = df_ven.drop_duplicates()
        df_ven.columns = ven_cols.values()

        return ContractData(po=df_po, vendor=df_ven)

    def get_sharepoint_data(self) -> ContractData:
        """Get current POs and Vendors from their respective SharePoint lists

        Returns
        -------
        ContractData
            A ContractData instance of the PO and vendor data from CitiBuy
        """
        # get the SharePoint list clients
        ven_list = self.sharepoint.get_list("Vendors")
        po_list = self.sharepoint.get_list("Purchase Orders")

        # retrieve the list of vendors
        df_ven = ven_list.get_items().to_dataframe(include_id=True)

        # retrieve the list of POs
        # TODO: Add support for "not in" filter
        po_open = {"Status": ("not equals", "3PCO - Closed")}
        df_po = po_list.get_items(query=po_open).to_dataframe(include_id=True)

        return ContractData(po=df_po, vendor=df_ven)

    def update_sharepoint(
        self,
        citibuy_data: pd.DataFrame,
        sharepoint_data: pd.DataFrame,
    ) -> BatchedChanges:
        """Compares the lists of vendors pulled from CitiBuy to the vendors
        in SharePoint and returns a list of the changes to make in SharePoint

        Parameters
        ----------
        citibuy_data: ContractData
            An instance of ContractData for the new PO and Vendor records
            retrieved from CitiBuy
        sharepoint_data: ContractData
            An instance of ContractData for the existing PO and Vendor records
            in SharePoint
        """
        # extract the old and new datasets
        new_po = citibuy_data.po.replace({np.nan: None})
        old_po = sharepoint_data.po.replace({np.nan: None})
        new_ven = citibuy_data.vendor
        old_ven = sharepoint_data.vendor

        # update the list of vendors
        ven_changes = self.detect_changes(
            old_ven.to_dict("records"),
            new_ven.to_dict("records"),
            key_col="Vendor ID",
        )
        print("VEN UPDATES")
        pprint(ven_changes.updates)
        print("VEN INSERTS")
        pprint(ven_changes.inserts)
        # ven_updates = ven_list.batch_upsert(changes)

        # # extract new lookup ids from batch upsert
        # new_lookup_ids = {}
        # for update in ven_updates:
        #     if update["status"] == 201:
        #         # TODO: Extract Vendor ID and lookup id
        #         pass

        # create mapping for VendorLookupId
        # which is needed to populate a lookup field in SharePoint
        ven_ids = old_ven[["id", "Vendor ID"]].to_dict("records")
        old_lookup_ids = {item["Vendor ID"]: item["id"] for item in ven_ids}
        ven_lookup = {**old_lookup_ids}

        # filter for POs that were closed in CitiBuy since the last run
        po_closed = old_po[~old_po["Title"].isin(new_po["Title"])].copy()
        po_closed["Status"] = "3PCO - Closed"

        # filter for POs that were created in CitiBuy since the last run
        po_created = new_po[~new_po["Title"].isin(old_po["Title"])].copy()
        po_created["Vendor ID"] = po_created["Vendor ID"].replace(ven_lookup)
        po_created = po_created.rename(columns={"Vendor ID": "VendorLookupId"})

        # filter for POs that already existed in SharePoint
        po_exists = new_po[new_po["Title"].isin(old_po["Title"])].copy()
        po_exists = po_exists.drop(columns="Vendor ID")

        # update closed POs
        po_closings = BatchedChanges()
        for po in po_closed.to_dict("records"):
            po_closings.updates[po["id"]] = {"Status": po["Status"]}
        print("CLOSINGS")
        pprint(po_closings.updates)

        # insert new POs
        po_inserts = BatchedChanges(inserts=po_created.to_dict("records"))
        print("PO INSERTS")
        pprint(po_inserts.inserts)

        # update existing POs
        po_changes = self.detect_changes(
            old_po.to_dict("records"),
            po_exists.to_dict("records"),
            key_col="Title",
        )
        print("PO CHANGES")
        pprint(po_changes.updates)

    def detect_changes(
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
