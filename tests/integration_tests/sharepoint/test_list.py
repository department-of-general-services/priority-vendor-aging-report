import pytest

from aging_report.sharepoint import ListItem, ItemCollection

ITEM_KEY = {"PO Number": "P12345:12", "Invoice Number": "12345"}
QUERY = {"PO Number": ("equals", "P12345:12")}


@pytest.fixture(scope="module", name="test_list")
def fixture_list(test_sharepoint):
    """Creates an instance of SiteList for use in integration tests"""
    return test_sharepoint.get_list("Priority Vendor Aging")


class TestSiteList:
    """Tests the SiteList methods that make calls to the Graph API"""

    def test_get_items(self, test_list):
        """Tests that the get_items() method executes correctly

        Validates the following conditions:
        - The response returned is a dictionary of InvoiceItem instances
        - The correct set of items are returned
        """
        # execution
        items = test_list.get_items(query=QUERY)
        print(items.items[0].fields)
        # validation
        assert len(items.items) == 3
        assert isinstance(items, ItemCollection)
        assert isinstance(items.items[0], ListItem)

    def test_get_invoice_by_key(self, test_list):
        """Tests that the get_invoice_by_key method executes correctly

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
        """Tests that the get_invoice_by_key method raises a ValueError if
        attempting to get an item with no matching key
        """
        # setup
        fake_key = {"PO Number": "Fake", "Invoice Number": "Fake"}
        with pytest.raises(ValueError):
            test_list.get_item_by_key(fake_key)


class TestInvoiceItem:
    """Tests the InvoiceItem methods that make calls to Graph API"""

    def test_update(self, test_list):
        """Tests that InvoiceItem.update executes successfully

        Validates the following conditions:
        - InvoiceItem.update() doesn't throw an error
        - The field was successfully updated in SharePoint
        """
        # setup - get invoice
        invoice = test_list.get_item_by_key(ITEM_KEY)
        status = invoice.get("Status")
        # setup - set update dict
        if status == "8. Paid":
            data = {"Status": "Error"}
        else:
            data = {"Status": "8. Paid"}
        # execution
        invoice.update(data)
        result = test_list.get_item_by_key(ITEM_KEY)
        new_status = result.get("Status")
        # validation
        assert status != new_status
        assert new_status == data["Status"]
