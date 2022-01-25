import pytest
import pandas as pd

from dgs_fiscal.etl import AgingReport
from dgs_fiscal.systems import SharePoint
from dgs_fiscal.etl.aging_report import constants
from tests.unit_tests.citibuy import data


@pytest.fixture(scope="session", name="mock_aging")
def fixture_aging_report(mock_db):
    """Mocks the ContractManagement class with the local CitiBuy db"""
    return AgingReport(citibuy_url=mock_db)


class TestAgingReport:
    """Tests the AgingReport class"""

    def test_init(self, mock_aging):
        """Tests that AgingReport class inits correctly

        Validates the following conditions:
        - The AgingReport class was instantiated with the mock_db
        - AgingReport.sharepoint is an instance of the SharePoint class
        """
        # execution
        records = mock_aging.citibuy.get_purchase_orders().records
        # validation
        assert len(records) == 7
        assert isinstance(mock_aging.sharepoint, SharePoint)

    def test_get_citibuy_data(self, mock_aging):
        """Tests that the get_citibuy_data() method executes correctly

        Validates the following conditions:
        - The correct set of invoices are returned from CitiBuy
        - Each record has all of the necessary fields
        """
        # setup
        cols = constants.CITIBUY["invoice_cols"]
        expected = pd.DataFrame(data.INVOICE_RESULTS)[cols.keys()]
        expected.columns = cols.values()
        # execution
        output = mock_aging.get_citibuy_data()
        print(output)
        # validation
        assert output.columns.all() == expected.columns.all()
        for val in output["Status"]:
            assert val in mock_aging.citibuy.INVOICE_STATUS.values()
