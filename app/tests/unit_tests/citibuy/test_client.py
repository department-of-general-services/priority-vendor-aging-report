from pprint import pprint

import pytest
import sqlalchemy

from tests.unit_tests.citibuy import data
from dgs_fiscal.systems import CitiBuy
import dgs_fiscal.etl.aging_report.constants as aging_constants


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
        """Tests that CitiBuy.get_purchase_orders() returns all records when no
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
        CitiBuy.get_purchase_orders()

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
        """Tests that CitiBuy.get_invoices() returns all records when no
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
        columns = aging_constants.CITIBUY["invoice_cols"].keys()
        # execution
        output = mock_citibuy.get_invoices().records
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        output_cols = output[0].keys()
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert len(output) == len(expected)
        assert output == expected
        for col in columns:
            if col == "po_type":
                continue
            assert col in output_cols

    def test_query_custom_date_range(self, mock_citibuy):
        """Tests that CitiBuy.get_invoices() returns more records when the
        days_ago parameter is passed a large value

        Validates the following conditions:
        - The results exclude invoices that were cancelled or paid up to 5000
          days ago
        """
        # setup
        filtered = data.INVOICE_RESULTS
        old_invoice = "invoice1"  # an invoice paid more than 90 days ago
        # execution
        output = mock_citibuy.get_invoices(days_ago=5000).records
        invoice_ids = [record["id"] for record in output]
        print("OUTPUT")
        pprint(output)
        # validation
        assert len(output) >= len(filtered)  # ensure more results are returned
        assert old_invoice in invoice_ids


class TestGetReceipts:
    """Tests the CitiBuy.get_receipts() method"""

    def test_get_receipts(self, mock_citibuy):
        """Tests that the get_receipts() method executes successfully"""
        # setup
        expected = data.RECEIPT_RESULTS
        # execution
        output = mock_citibuy.get_receipts().records
        pprint(output)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert len(output) == len(expected)
        assert output == expected
