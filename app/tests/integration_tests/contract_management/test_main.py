import pytest
import pandas as pd

from dgs_fiscal.etl import ContractManagement
from dgs_fiscal.etl.contract_management import ContractData, constants

from tests.integration_tests.contract_management import data


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
        assert len(records) == 5

    def test_get_citibuy_data(self, mock_contract):
        """Tests the get_citibuy_data() method executes correctly

        Validates the following conditions:
        - The return type is ContractData
        - The columns of ContractData.po match the CITIBUY constants
        - The columns of ContractData.vendor match the CITIBUY constants
        - The dataframe in ContractData.vendor has been deduped
        - The PO Type has been set correctly
        """
        # setup
        po_cols = list(constants.CITIBUY["po_cols"].values())
        ven_cols = list(constants.CITIBUY["vendor_cols"].values())
        con_cols = list(constants.CITIBUY["contract_cols"].values())
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
        print(df_po.dtypes)
        print(df_ven.dtypes)
        print(df_con.dtypes)
        blanket_title = df_po.loc[0, "Title"]
        release_title = df_po.loc[1, "Title"]
        # validation
        assert isinstance(output, ContractData)
        assert list(df_po.columns) == po_cols
        assert list(df_ven.columns) == ven_cols
        assert list(df_con.columns) == con_cols
        assert len(df_ven) == 2
        assert blanket_title == "P111"
        assert release_title == "P111:1"
        assert list(df_po["PO Type"]) == po_types

    def test_get_sharepoint_data(self, mock_contract):
        """Tests the get_sharepoint_data() method executes correctly

        Validates the following conditions:
        - The return type is ContractData
        - The Vendor column in the PO data has been matched with Vendor ID
        - The names of the columns match the output of get_citibuy_data()
        """
        # setup
        po_cols = list(constants.CITIBUY["po_cols"].values())
        ven_cols = list(constants.CITIBUY["vendor_cols"].values())
        po_cols.remove("Vendor ID")
        # execution
        output = mock_contract.get_sharepoint_data()
        print(output.po)
        print(output.vendor)
        # validation
        assert isinstance(output, ContractData)
        assert "id" in output.po.columns
        assert "id" in output.vendor.columns
        for col in ven_cols:
            assert col in output.vendor.columns
        for col in po_cols:
            assert col in output.po.columns

    def test_reconcile_lists(self, mock_contract):
        """Tests that the reconcile_lists() method executes correctly

        Validates the following conditions:
        -
        """
        # setup
        po_citibuy = pd.DataFrame(data.CITIBUY["po"])
        ven_citibuy = pd.DataFrame(data.CITIBUY["vendor"])
        con_citibuy = pd.DataFrame(data.CITIBUY["contract"])
        po_sharepoint = pd.DataFrame(data.SHAREPOINT["po"])
        ven_sharepoint = pd.DataFrame(data.SHAREPOINT["vendor"])
        con_sharepoint = pd.DataFrame(data.SHAREPOINT["contract"])
        citibuy = ContractData(
            po=po_citibuy,
            vendor=ven_citibuy,
            contract=con_citibuy,
        )
        sharepoint = ContractData(
            po=po_sharepoint,
            vendor=ven_sharepoint,
            contract=con_sharepoint,
        )
        # execution
        output = mock_contract.update_sharepoint(citibuy, sharepoint)
        print(output)
        # validation
        assert 1
