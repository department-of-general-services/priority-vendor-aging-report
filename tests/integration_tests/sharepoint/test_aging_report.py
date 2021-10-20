# pylint: disable=W0212
import pytest

from aging_report.sharepoint import ListItem

INVOICE_KEY = {"PO Number": "P12345:12", "Invoice Number": "12345"}
QUERY = {"PO Number": ("equals", "P12345:12")}


@pytest.fixture(scope="session", name="test_report")
def fixture_report(test_sharepoint):
    """Creates an instance of SiteList for use in integration tests"""
    return test_sharepoint.get_list("Priority Vendor Aging")


class TestSiteList:
    """Tests the SiteList methods that make calls to the Graph API"""

    def test_get_items(self, test_report):
        """Tests that the get_items() method executes correctly

        Validates the following conditions:
        - The response returned is a dictionary of InvoiceItem instances
        - The correct set of invoices are returned
        - The response matches the value of SiteList.invoices
        """
        # execution
        invoices = test_report.get_items(query=QUERY)
        print(invoices[0].fields)
        # validation
        assert len(invoices) == 3
        assert isinstance(invoices[0], ListItem)
        assert invoices == test_report.items

    def test_get_invoice_by_key_existing(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly when
        the invoice with that key is already in SiteList.invoices

        Validates the following conditions
        - The response returned is an instance of InvoiceItem
        - The response has the fields attribute set correctly
        """
        # setup
        test_report.get_items(query=QUERY)
        matches = test_report.find_items_by_field(INVOICE_KEY)
        assert matches != []
        # execution
        invoice = test_report.get_item_by_key(INVOICE_KEY)
        # validation
        assert isinstance(invoice, ListItem)
        assert isinstance(invoice.fields, dict)
        assert invoice == matches[0]

    def test_get_invoice_by_key_no_match(self, test_report):
        """Tests that the get_invoice_by_key method raises a ValueError if
        attempting to get an item with no matching key
        """
        # setup
        fake_key = {"PO Number": "Fake", "Invoice Number": "Fake"}
        matches = test_report.find_items_by_field(fake_key)
        assert matches == []
        with pytest.raises(ValueError):
            test_report.get_item_by_key(fake_key)

    def test_get_invoice_by_key_missing(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly when
        the invoice with that key isn't in SiteList.invoices

        Validates the following conditions
        - The response returned is an instance of InvoiceItem
        - The invoice has been added to SiteList.invoices
        - The response has the fields attribute set correctly
        """
        # setup
        test_report._items = {}  # removes all invoices
        # execution
        invoice = test_report.get_item_by_key(INVOICE_KEY)
        # validation
        assert isinstance(invoice, ListItem)
        assert isinstance(invoice.fields, dict)


class TestInvoiceItem:
    """Tests the InvoiceItem methods that make calls to Graph API"""

    def test_update(self, test_report):
        """Tests that InvoiceItem.update executes successfully

        Validates the following conditions:
        - InvoiceItem.update() doesn't throw an error
        - The field was successfully updated in SharePoint
        """
        # setup - get invoice
        invoice = test_report.get_item_by_key(INVOICE_KEY)
        status = invoice.get("Status")
        # setup - set update dict
        if status == "8. Paid":
            data = {"Status": "Error"}
        else:
            data = {"Status": "8. Paid"}
        # execution
        invoice.update(data)
        # resets item list to retrieve invoice from SharePoint
        test_report._items = {}
        result = test_report.get_item_by_key(INVOICE_KEY)
        new_status = result.get("Status")
        # validation
        assert status != new_status
        assert new_status == data["Status"]
