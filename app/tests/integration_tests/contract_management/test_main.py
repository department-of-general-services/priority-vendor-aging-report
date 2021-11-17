import pytest

from dgs_fiscal.etl import ContractManagement
from dgs_fiscal.etl.contract_management import ContractData, constants


@pytest.fixture(scope="session", name="mock_contract")
def fixture_contract(mock_db):
    """Mocks the ContractManagement class with the local CitiBuy db"""
    return ContractManagement(citibuy_url=mock_db)


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
        """
        # setup
        po_cols = list(constants.CITIBUY["po_cols"].values())
        ven_cols = list(constants.CITIBUY["vendor_cols"].values())
        # execution
        output = mock_contract.get_citibuy_data()
        df_po = output.po
        df_ven = output.vendor
        blanket_title = df_po.loc[0, "Title"]
        release_title = df_po.loc[1, "Title"]
        # validation
        assert isinstance(output, ContractData)
        assert list(df_po.columns) == po_cols
        assert list(df_ven.columns) == ven_cols
        assert len(df_ven) == 2
        assert blanket_title == "P111"
        assert release_title == "P111:1"
        # validation
        assert isinstance(output, ContractData)
        assert list(output.po.columns) == po_cols
        assert list(output.vendor.columns) == ven_cols
        assert len(output.vendor) == 2
