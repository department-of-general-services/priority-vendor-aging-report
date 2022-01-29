from pprint import pprint

import pytest
import pandas as pd

from dgs_fiscal.systems.sharepoint import BatchedChanges
from dgs_fiscal.etl import ContractManagement
from dgs_fiscal.etl.contract_management import ContractData, constants

from tests.integration_tests.contract_management import data

PO_COLS = list(constants.CITIBUY["po_cols"].values())
VEN_COLS = list(constants.CITIBUY["vendor_cols"].values())
CON_COLS = list(constants.CITIBUY["contract_cols"].values())
VEN_MAPPING = {"111": "1", "222": "2", "333": "11"}
CON_MAPPING = {"P111": "1", "P222": "2", "P333": "3"}


@pytest.fixture(scope="session", name="mock_contract")
def fixture_contract(mock_db):
    """Mocks the ContractManagement class with the local CitiBuy db"""
    contract = ContractManagement(
        citibuy_url=mock_db,
        po_list="Purchase Orders Test",
        vendor_list="Vendors Test",
        contract_list="Master Blanket POs Test",
    )
    return contract


class TestContractManagement:
    """Tests the ContractManagement class methods"""

    def test_init(self, mock_contract):
        """Tests that the ContractManagement class inits correctly with the
        mock CitiBuy database
        """
        # execution
        records = mock_contract.citibuy.get_purchase_orders().records
        # validation
        assert len(records) == 7

    def test_get_citibuy_data(self, mock_contract):
        """Tests the get_citibuy_data() method executes correctly

        Validates the following conditions:
        - The return type is ContractData
        - The columns of ContractData.po match the CITIBUY constants
        - The columns of ContractData.vendor match the CITIBUY constants
        - The dataframe in ContractData.vendor has been deduped
        - The PO Type has been set correctly
        - The list of contracts excludes Open Market POs
        - The list of records in each dataframe is unique
        """
        # setup
        po_types = [
            "Master Blanket",
            "Release",
            "Master Blanket",
            "Release",
            "Open Market",
        ]
        # execution
        output = mock_contract.get_citibuy_data()
        df_po = output.po
        df_ven = output.vendor
        df_con = output.contract
        print(df_po)
        print(df_ven)
        print(df_con)
        blanket_title = df_po.loc[0, "Title"]
        release_title = df_po.loc[1, "Title"]
        # validation
        assert isinstance(output, ContractData)
        assert list(df_po.columns) == PO_COLS
        assert list(df_ven.columns) == VEN_COLS
        assert list(df_con.columns) == CON_COLS
        assert len(df_ven) == 2
        assert "P555" not in list(df_con["Title"])
        assert blanket_title == "P111"
        assert release_title == "P111:1"
        assert list(df_po["PO Type"]) == po_types
        assert list(df_con["Locations"]) is not None
        assert list(df_ven["Agency Locations"]) is not None
        for df in [df_po, df_ven, df_con]:
            assert len(df) == len(df["Title"].unique())
        for col in ["End Date", "Start Date"]:
            assert "T00:00:00Z" in df_con.loc[0, col]

    def test_get_sharepoint_data(self, mock_contract):
        """Tests the get_sharepoint_data() method executes correctly

        Validates the following conditions:
        - The return type is ContractData
        - The Vendor column in the PO data has been matched with Vendor ID
        - The names of the columns match the output of get_citibuy_data()
        """
        # execution
        output = mock_contract.get_sharepoint_data()
        print(output.po)
        print(output.contract)
        print(output.vendor)
        # validation
        assert isinstance(output, ContractData)
        assert "id" in output.po.columns
        assert "id" in output.vendor.columns
        for col in VEN_COLS:
            assert col in output.vendor.columns
        for col in PO_COLS:
            assert col in output.po.columns
        for col in CON_COLS:
            assert col in output.contract.columns
        for col in ["End Date", "Start Date"]:
            assert "T00:00:00Z" in output.contract.loc[0, col]


@pytest.mark.skip
class TestUpdateLists:
    """Tests the class methods that update the items in sharepoint lists
    for Vendors, Contracts, and Purchase Orders
    """

    def test_update_vendor_list(self, mock_contract):
        """Tests that the update_vendor_list() method executes correctly

        Validates the following conditions:
        - It returns a dictionary that maps vendor IDs to list item ids
        - The BatchedChanges instance contains the correct set of updates and
          inserts
        - The method returns a mapping of vendor ids to list item ids and a
          dictionary the BatchedChanges keyed by type of change
        """
        # setup
        citibuy = pd.DataFrame(data.CITIBUY["vendor"])
        sharepoint = pd.DataFrame(data.SHAREPOINT["vendor"])
        # execution
        output = mock_contract.update_vendor_list(
            old=sharepoint,
            new=citibuy,
        )
        mapping = output.mapping
        inserts = output.upserts["upserts"].inserts
        updates = output.upserts["upserts"].updates
        results = output.results
        pprint(results)
        pprint(mapping)
        pprint(inserts)
        pprint(updates)
        # validation
        assert set(mapping.keys()) == set(VEN_MAPPING.keys())
        assert mapping.get("333") is not None
        assert len(inserts) == 1
        assert list(updates.keys()) == ["1"]

    def test_update_po_list(self, mock_contract):
        """Tests that the update_po_list() method executes correctly

        Validates the following conditions:
        - It returns a dictionary that maps Title to list item ids
        - The BatchedChanges instance contains the correct set of updates and
          inserts
        - The method returns a mapping of PO numbers to list item ids and a
          dictionary the BatchedChanges keyed by type of change
        """
        # setup - create dummy data
        po_mapping = {
            "P111",
            "P111:1",
            "P111:2",
            "P222",
            "P444",
            "P111:3",
            "P333",
        }
        citibuy = pd.DataFrame(data.CITIBUY["po"])
        sharepoint = pd.DataFrame(data.SHAREPOINT["po"])
        # setup - make sure dummy cols match constants
        assert list(citibuy.columns) == PO_COLS
        for col in PO_COLS:
            assert col in sharepoint.columns
        # execution
        output = mock_contract.update_po_list(
            old=sharepoint,
            new=citibuy,
            vendor_lookup=VEN_MAPPING,
            contract_lookup=CON_MAPPING,
        )
        mapping = output.mapping
        updates = output.upserts["updates"]
        inserts = output.upserts["inserts"]
        closings = output.upserts["closings"]
        results = output.results
        pprint(results)
        pprint(mapping)
        pprint(inserts.inserts)
        pprint(updates.updates)
        pprint(closings.updates)
        # validation
        assert set(mapping.keys()) == po_mapping
        for po_nbr in ["P111:3", "P333", "P444"]:
            assert mapping.get(po_nbr) is not None
        assert len(inserts.inserts) == 3
        assert len(inserts.updates) == 0
        assert list(updates.updates.keys()) == ["3"]
        assert len(updates.inserts) == 0
        assert list(closings.updates.keys()) == ["2", "4"]
        assert len(closings.inserts) == 0
        for kind in ["updates", "inserts", "closings"]:
            assert isinstance(output.upserts[kind], BatchedChanges)

    def test_update_contract_list(self, mock_contract):
        """Tests that the update_contract_list() method executes correctly

        Validates the following conditions:
        - It returns a dictionary that maps PO Numbers to list item ids
        - The BatchedChanges instance contains the correct set of updates and
          inserts
        - The method returns a mapping of PO numbers to list item ids and a
          dictionary the BatchedChanges keyed by type of change
        """
        # setup
        citibuy = pd.DataFrame(data.CITIBUY["contract"])
        sharepoint = pd.DataFrame(data.SHAREPOINT["contract"])
        # setup - make sure dummy cols match constants
        assert list(citibuy.columns) == CON_COLS
        for col in CON_COLS:
            assert col in sharepoint.columns
        # execution
        output = mock_contract.update_contract_list(
            old=sharepoint,
            new=citibuy,
            vendor_lookup=VEN_MAPPING,
        )
        mapping = output.mapping
        updates = output.upserts["updates"]
        inserts = output.upserts["inserts"]
        results = output.results
        pprint(mapping)
        pprint(updates.updates)
        pprint(inserts.inserts)
        pprint(results)
        # validation
        assert set(mapping.keys()) == set(CON_MAPPING.keys())
        assert mapping.get("P333") is not None
        assert list(updates.updates.keys()) == ["1"]
        assert len(updates.inserts) == 0
        assert len(inserts.inserts) == 1
        assert len(inserts.updates) == 0
        assert isinstance(output.upserts["updates"], BatchedChanges)
        assert isinstance(output.upserts["inserts"], BatchedChanges)
