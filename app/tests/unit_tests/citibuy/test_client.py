from pprint import pprint

import pytest
import pandas as pd
import numpy as np
import sqlalchemy

from tests.utils import citibuy_data as data
from dgs_fiscal.systems import CitiBuy


@pytest.fixture(scope="session", name="mock_citibuy")
def fixture_mock_citibuy(mock_db):
    """Creates a mock instance of CitiBuy class for unit testing"""
    return CitiBuy(conn_url=mock_db)


@pytest.fixture(scope="module", name="mock_po_data")
def fixture_data():
    """Joins data from the PurchaseOrder, Vendor, and BlanketContract models
    and returns it as a list of dictionaries
    """
    # read in data
    po = pd.DataFrame(data.PURCHASE_ORDERS)
    vendors = pd.DataFrame(data.VENDORS)
    vendors = vendors.rename({"id": "vendor_id"}, axis="columns")
    contracts = pd.DataFrame(data.BLANKET_CONTRACTS)

    # merge data
    df = po.merge(vendors, on="vendor_id", how="left")
    df = df.merge(contracts, on=["po_nbr", "release_nbr"], how="left")
    df = df.fillna(np.nan).replace([np.nan], [None])
    df = df[df["agency"] != "DPW"]
    return df


class TestCitiBuy:
    """Unit tests for the CitiBuy class"""

    def test_init(self, mock_citibuy):
        """Tests that the mock CitiBuy db was populated correctly"""
        # validation
        assert isinstance(mock_citibuy.engine, sqlalchemy.engine.Engine)
        with pytest.raises(NotImplementedError):
            print(mock_citibuy.purchase_orders)
        with pytest.raises(NotImplementedError):
            print(mock_citibuy.vendors)
        with pytest.raises(NotImplementedError):
            print(mock_citibuy.invoices)


class TestGetPurchaseOrders:
    """Tests the CitiBuy.get_purchase_orders() method"""

    def test_query_default(self, mock_citibuy, mock_po_data):
        """Tests that PurchaseOrders.get_records() returns all records when no
        values are passed to the filter or limit paramaters

        Validates the following conditions:
        - All purchase order records are returned
        - The results are returned as a list of dictionary items
        - The dictionary for each record also includes fields from the Vendor
          and BlanketContract tables
        """
        # setup
        expected = mock_po_data.to_dict("records")
        # execution
        output = mock_citibuy.get_purchase_orders()
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert output == expected
        assert output == mock_citibuy.purchase_orders

    def test_get_records_limit(self, mock_citibuy, mock_po_data):
        """Tests that the limit parameter works as expected when passed to
        PurchaseOrder.get_records()

        Validates the following conditions:
        - Only the first x records are returned when a limit of x is passed
        """
        # setup
        expected = mock_po_data.head(1).to_dict("records")
        # execution
        output = mock_citibuy.get_purchase_orders(limit=1)
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert output == expected
