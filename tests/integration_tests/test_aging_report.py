from pprint import pprint

import pytest
import requests
from O365 import Account
from O365.sharepoint import Sharepoint, Site, SharepointList

from aging_report.config import settings
from aging_report.errors import ColumnNotFound
from aging_report.sharepoint import (
    Client,
    FiscalSite,
    AgingReportList,
    AgingReportItem,
)


class TestClient:
    """Tests the Client methods that make external calls to Graph API"""

    def test_init(self, test_client):
        """Tests that Client instantiates correctly

        Validatees the following conditions:
        - Client.account exists and is an instance of O365.Account
        - Client.app exists and is an instance of O365.Sharepoint
        - Client.account is authenticated with Graph API
        """
        # validation
        assert isinstance(test_client.account, Account)
        assert isinstance(test_client.app, Sharepoint)
        assert test_client.is_authenticated

    def test_get_fiscal_site(self, test_client):
        """Tests that Client.get_fiscal_site() returns a DGSFiscal instance

        Validates the following conditions:
        - The response returned is an instance of DGSFiscal
        - DGSFiscal.site exists and is an instance of O365.Site
        - The SharePoint site retrieved has the correct url
        """
        # execution
        fiscal = test_client.get_fiscal_site()
        # validation
        assert isinstance(fiscal, FiscalSite)
        assert isinstance(fiscal.site, Site)
        assert "Fiscal" in fiscal.site.web_url

    def test_get_aging_report(self, test_client):
        """Tests that Client.get_aging_report() returns an AgingReportList instance

        Validates the following conditions:
        - The response returned is an instance of AgingReportList
        - AgingReportList.list exists and is an instance of O365.SharepointList
        - The SharePoint list retrieved has the correct name
        """
        # execution
        report = test_client.get_aging_report()
        # validation
        assert isinstance(report, AgingReportList)
        assert isinstance(report.list, SharepointList)
        assert report.list.name == "Priority Vendor Aging"


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
