from pprint import pprint

import pytest
import sqlalchemy

from tests.unit_tests.citibuy import data
from dgs_fiscal.systems import CitiBuy


@pytest.fixture(scope="session", name="mock_citibuy")
def fixture_mock_citibuy(mock_db):
    """Creates a mock instance of CitiBuy class for unit testing"""
    return CitiBuy(conn_url=mock_db)


class TestCitiBuy:
    """Unit tests for the CitiBuy class"""

    def test_init(self, mock_citibuy):
        """Tests that the mock CitiBuy db was populated correctly"""
        # validation
        assert isinstance(mock_citibuy.engine, sqlalchemy.engine.Engine)


class TestGetPurchaseOrders:
    """Tests the CitiBuy.get_purchase_orders() method"""

    def test_query_default(self, mock_citibuy):
        """Tests that PurchaseOrders.get_records() returns all records when no
        values are passed to the filter or limit paramaters

        Validates the following conditions:
        - All purchase order records are returned
        - The results are returned as a list of dictionary items
        - The dictionary for each record also includes fields from the Vendor
          and BlanketContract tables
        """
        # setup
        expected = data.PO_RESULTS
        # execution
        output = mock_citibuy.get_purchase_orders().records
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert len(output) == len(expected)
        assert output == expected

    def test_get_records_limit(self, mock_citibuy):
        """Tests that the limit parameter works as expected when passed to
        PurchaseOrder.get_records()

        Validates the following conditions:
        - Only the first x records are returned when a limit of x is passed
        """
        # setup
        expected = data.PO_RESULTS[:1]
        # execution
        output = mock_citibuy.get_purchase_orders(limit=1).records
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert output == expected


class TestGetInvoices:
    """Tests the CitiBuy.get_invoices() method"""

    def test_query_default(self, mock_citibuy):
        """Tests that PurchaseOrders.get_records() returns all records when no
        values are passed to the filter or limit paramaters

        Validates the following conditions:
        - All matching invoices are returned with the correct fields
        - The results are returned as a list of dictionary items
        - The results exclude invoices that were cancelled or paid more than
          45 days ago
        - The results exclude invoices on POs from other agencies
        """
        # setup
        expected = data.INVOICE_RESULTS
        # execution
        output = mock_citibuy.get_invoices().records
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert len(output) == len(expected)
        assert output == expected
