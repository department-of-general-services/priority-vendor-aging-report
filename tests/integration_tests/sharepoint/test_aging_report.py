from aging_report.sharepoint import AgingReportItem


class TestAgingReportList:
    """Tests the AgingReportList methods that make calls to the Graph API"""

    def test_get_invoices(self, test_report):
        """Tests that the get_invoices() method executes correctly

        Validates the following conditions:
        - The response returned is a dictionary of AgingReportItem instances
        - The correct set of invoices are returned
        - The response matches the value of AgingReportList.invoices
        """
        # setup
        po_num = "P12345:12"
        invoice_num = "12345"
        invoice_key = (po_num, invoice_num)
        # execution
        # query = {"PO Number": ("equals", "P12345:12")}
        invoices = test_report.get_invoices()
        # validation
        assert isinstance(invoices.get(invoice_key), AgingReportItem)
        assert invoices == test_report.invoices

    def test_get_invoice_by_key_existing(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly when
        the invoice with that key is already in AgingReportList.invoices

        Validates the following conditions
        - The response returned is an instance of AgingReportItem
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
        assert isinstance(invoice, AgingReportItem)
        assert isinstance(invoice.fields, dict)

    def test_get_invoice_by_key_missing(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly when
        the invoice with that key isn't in AgingReportList.invoices

        Validates the following conditions
        - The response returned is an instance of AgingReportItem
        - The invoice has been added to AgingReportList.invoices
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
        assert isinstance(invoice, AgingReportItem)
        assert isinstance(invoice.fields, dict)
        assert invoice_key in test_report.invoices
