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
        invoices = test_report.get_invoices()
        # validation
        assert len(invoices) == 3
        assert isinstance(invoices.get(invoice_key), AgingReportItem)
        assert invoices == test_report.invoices

    def test_get_invoice_by_key(self, test_report):
        """Tests that the get_invoice_by_key method executes correctly

        Validates the following conditions
        - The response returned is an instance of AgingReportItem
        - The invoice has been added to AgingReportList.invoices
        """
        # setup
        po_num = "P12345:12"
        invoice_num = "12345"
        invoice_key = (po_num, invoice_num)
        # execution
        invoice = test_report.get_invoice_by_key(po_num, invoice_num)
        # validation
        assert invoice_key in test_report.invoices
        assert isinstance(invoice, AgingReportItem)
        assert isinstance(invoice.fields, dict)
