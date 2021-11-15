import pytest

from dgs_fiscal.etl import ContractManagement
from dgs_fiscal.etl.contract_management import ContractData
from tests.integration_tests.contract_management import data


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
