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
        - The columns of ContractData.po match the constants
        - The columns of ContractData.vendor match the constants
        - The dataframe in ContractData.vendor has been deduped
        """
        # setup
        po_cols = list(constants.CITIBUY["po_cols"].values())
        ven_cols = list(constants.CITIBUY["vendor_cols"].values())
        # validation
        output = mock_contract.get_citibuy_data()
        # validation
        assert isinstance(output, ContractData)
        assert list(output.po.columns) == po_cols
        assert list(output.vendor.columns) == ven_cols
        assert len(output.vendor) == 2
