from pprint import pprint

import pytest
import sqlalchemy
import pandas as pd
import numpy as np

from tests.utils import citibuy_data as data


@pytest.fixture(scope="module", name="mock_data")
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


class TestPurchaseOrders:
    """Tests the PurchaseOrder class methods"""

    def test_init(self, mock_po):
        """Tests that the PurchaseOrders method inits correctly

        Validates the following test conditions:
        - The class instance inherits self.engine from the CitiBuy class
        - The attribute self.sharepoint is None
        - The attribute self.records is an empty list
        """
        # validation
        assert isinstance(mock_po.engine, sqlalchemy.engine.Engine)
        assert mock_po.sharepoint is None
        with pytest.raises(AttributeError):
            print(mock_po.records)

    def test_get_records_all(self, mock_po, mock_data):
        """Tests that PurchaseOrders.get_records() returns all records when no
        values are passed to the filter or limit paramaters

        Validates the following conditions:
        - All purchase order records are returned
        - The results are returned as a list of dictionary items
        - The dictionary for each record also includes fields from the Vendor
          and BlanketContract tables
        """
        # setup
        expected = mock_data.to_dict("records")
        # execution
        output = mock_po.get_records()
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert output == expected

    def test_get_records_limit(self, mock_po, mock_data):
        """Tests that the limit parameter works as expected when passed to
        PurchaseOrder.get_records()

        Validates the following conditions:
        - Only the first x records are returned when a limit of x is passed
        """
        # setup
        expected = mock_data.head(1).to_dict("records")
        # execution
        output = mock_po.get_records(limit=1)
        print("OUTPUT")
        pprint(output)
        print("EXPECTED")
        pprint(expected)
        # validation
        assert output == expected
