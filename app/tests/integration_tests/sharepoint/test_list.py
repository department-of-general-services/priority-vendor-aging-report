import pytest
import pandas as pd

from dgs_fiscal.systems.sharepoint.list import ListItem, ItemCollection

ITEM_KEY = {"PO Number": "P12345:12", "Invoice Number": "12345"}
QUERY = {"PO Number": ("equals", "P12345:12")}


@pytest.fixture(scope="module", name="test_list")
def fixture_list(test_sharepoint):
    """Creates an instance of SiteList for use in integration tests"""
    return test_sharepoint.get_list("Priority Vendor Aging")


@pytest.fixture(scope="module", name="test_items")
def fixture_items(test_list):
    """Returns an instance of ItemCollection for testing"""
    return test_list.get_items(query=QUERY)


class TestSiteList:
    """Tests the SiteList methods that make calls to the Graph API"""

    def test_get_items(self, test_items):
        """Tests that the get_items() method executes correctly

        Validates the following conditions:
        - The response returned is a dictionary of InvoiceItem instances
        - The correct set of items are returned
        """
        # validation
        print(test_items.items[0].fields)
        assert len(test_items.items) == 3
        assert isinstance(test_items, ItemCollection)
        assert isinstance(test_items.items[0], ListItem)

    def test_get_invoice_by_key(self, test_list):
        """Tests that the get_invoice_by_key() method executes correctly

        Validates the following conditions
        - The response returned is an instance of ListItem
        - The response has the fields attribute set correctly
        """
        # execution
        invoice = test_list.get_item_by_key(ITEM_KEY)
        # validation
        assert isinstance(invoice, ListItem)
        assert isinstance(invoice.fields, dict)

    def test_get_invoice_by_key_no_match(self, test_list):
        """Tests that the get_invoice_by_key() method raises a ValueError if
        attempting to get an item with no matching key
        """
        # setup
        fake_key = {"PO Number": "Fake", "Invoice Number": "Fake"}
        with pytest.raises(ValueError):
            test_list.get_item_by_key(fake_key)

    def test_add_item(self, test_list):
        """Tests that the add_items() method executes correctly

        Validates the following conditions:
        - The item has been created in SharePoint
        - The method returns the items as an ItemCollection
        """
        # setup
        test_data = {"PO Number": "new item", "Invoice Number": "new item"}
        # execution
        item = test_list.add_item(test_data)
        # validation
        try:
            assert isinstance(item, ListItem)
            for key, val in test_data.items():
                assert item.get_val(key) == val
        except AssertionError as err:
            raise err
        finally:
            # cleanup
            assert item.item.delete()

    def test_add_item_invalid(self, test_list):
        """Tests that add_item() raises a KeyError when it is provided data
        that has a key that isn't one of the list's existing columns
        """
        # setup
        test_data = {"Fake Col": "new item", "Invoice Number": "new item"}
        # validation
        with pytest.raises(KeyError):
            test_list.add_item(test_data)


class TestItemCollection:
    """Tests the ItemCollection class methods"""

    def test_filter_items_success(self, test_items):
        """Tests that ItemCollection.filter_items() executes successfully when
        passed a valid filter_key

        Validates the following conditions:
        - The correct number of invoices are returned
        - The invoices returned have fields that match the values passed in the
          filter key
        """
        # execution
        invoices = test_items.filter_items(ITEM_KEY)
        # validation
        assert len(invoices) == 1
        assert invoices[0].get_val("PO Number") == "P12345:12"
        assert invoices[0].get_val("Invoice Number") == "12345"

    def test_filter_items_invalid_field(self, test_items):
        """Tests that ItemCollection.filter_items() returns a KeyError when
        passed an invalid filter_key
        """
        # setup
        fake_key = {"Fake Key": "Key"}
        # validation
        with pytest.raises(KeyError):
            test_items.filter_items(fake_key)

    def test_to_dataframe(self, test_items):
        """Tests that ItemCollection.to_dataframe() executes correctly

        Validates the following conditions:
        - The method returns a dataframe
        - The columns have been renamed successfully
        - The dataframe has the correct number of rows
        """
        # execution
        df = test_items.to_dataframe()
        # validation
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert "PO Number" in df.columns
        assert "Invoice Number" in df.columns


class TestListItem:
    """Tests the ListItem methods that make calls to Graph API"""

    def test_update(self, test_list, test_items):
        """Tests that InvoiceItem.update executes successfully

        Validates the following conditions:
        - InvoiceItem.update() doesn't throw an error
        - The field was successfully updated in SharePoint
        """
        # setup - get invoice
        invoice = test_items.filter_items(ITEM_KEY)[0]
        status = invoice.get_val("Status")
        # setup - set update dict
        if status == "8. Paid":
            data = {"Status": "Error"}
        else:
            data = {"Status": "8. Paid"}
        # execution
        invoice.update(data)
        result = test_list.get_item_by_key(ITEM_KEY)
        new_status = result.get_val("Status")
        # validation
        assert status != new_status
        assert new_status == data["Status"]
