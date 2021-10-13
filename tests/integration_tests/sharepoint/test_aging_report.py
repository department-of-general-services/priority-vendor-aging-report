from aging_report.sharepoint import InvoiceItem


class TestInvoiceList:
    """Tests the InvoiceList methods that make calls to the Graph API"""

    def test_get_invoices(self, test_report):
        """Tests that the get_invoices() method executes correctly

        Validates the following conditions:
        - The response returned is a dictionary of InvoiceItem instances
        - The correct set of invoices are returned
        - The response matches the value of InvoiceList.invoices
        """
        # setup
        po_num = "P12345:12"
        invoice_num = "12345"
        invoice_key = (po_num, invoice_num)
        # execution
        query = {"PO Number": ("equals", "P12345:12")}
        invoices = test_report.get_invoices(query=query)
        # validation
        assert len(invoices) == 3
        assert isinstance(invoices.get(invoice_key), InvoiceItem)
        assert invoices == test_report.invoices

    def test_get_invoice_by_key_existing(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly when
        the invoice with that key is already in InvoiceList.invoices

        Validates the following conditions
        - The response returned is an instance of InvoiceItem
        - The response has the fields attribute set correctly
        """
        # setup
        po_num = "P12345:12"
        invoice_num = "12345"
        invoice_key = (po_num, invoice_num)
        assert invoice_key in test_report.invoices
        # execution
        invoice = test_report.get_invoice_by_key(po_num, invoice_num)
        # validation
        assert isinstance(invoice, InvoiceItem)
        assert isinstance(invoice.fields, dict)

    def test_get_invoice_by_key_missing(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly when
        the invoice with that key isn't in InvoiceList.invoices

        Validates the following conditions
        - The response returned is an instance of InvoiceItem
        - The invoice has been added to InvoiceList.invoices
        - The response has the fields attribute set correctly
        """
        # setup
        po_num = "P12345:12"
        invoice_num = "12345"
        invoice_key = (po_num, invoice_num)
        # setup - check that invoice key isn't in self.invoices
        if invoice_key in test_report.invoices:
            del test_report.invoices[invoice_key]
        assert invoice_key not in test_report.invoices
        # execution
        invoice = test_report.get_invoice_by_key(po_num, invoice_num)
        # validation
        assert isinstance(invoice, InvoiceItem)
        assert isinstance(invoice.fields, dict)
        assert invoice_key in test_report.invoices


class TestInvoiceItem:
    """Tests the InvoiceItem methods that make calls to Graph API"""

    def test_update(self, test_report):
        """Tests that InvoiceItem.update executes successfully

        Validates the following conditions:
        - InvoiceItem.update() doesn't throw an error
        - The field was successfully updated in SharePoint
        """
        # setup - get invoice
        fields = ("PONumber", "InvoiceNumber", "CitiBuyStatus")
        po_num = "P12345:12"
        invoice_num = "12345"
        invoice_key = (po_num, invoice_num)
        if invoice_key in test_report.invoices:
            del test_report.invoices[invoice_key]
        invoice = test_report.get_invoice_by_key(po_num, invoice_num, fields)
        status = invoice.fields["CitiBuyStatus"]
        # setup - set update dict
        if status == "8. Paid":
            data = {"Status": "Error"}
        else:
            data = {"Status": "8. Paid"}
        # execution
        invoice.update(data)
        del test_report.invoices[invoice_key]
        result = test_report.get_invoice_by_key(po_num, invoice_num, fields)
        # validation
        assert result.fields["CitiBuyStatus"] == data["Status"]
