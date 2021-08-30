from pprint import pprint

import pytest
import requests
from O365 import Account
from O365.sharepoint import Sharepoint, Site, SharepointList

from aging_report.config import settings
from aging_report.sharepoint import (
    Client,
    FiscalSite,
    AgingReportList,
    AgingReportItem,
)


class TestClient:
    """Tests the Client methods that make external calls to Graph API"""

    def test_init(self, client):
        """Tests that Client instantiates correctly

        Validatees the following conditions:
        - Client.account exists and is an instance of O365.Account
        - Client.app exists and is an instance of O365.Sharepoint
        - Client.account is authenticated with Graph API
        """
        # validation
        assert isinstance(client.account, Account)
        assert isinstance(client.app, Sharepoint)
        assert client.is_authenticated

    def test_get_fiscal_site(self, client):
        """Tests that Client.get_fiscal_site() returns a DGSFiscal instance

        Validates the following conditions:
        - The response returned is an instance of DGSFiscal
        - DGSFiscal.site exists and is an instance of O365.Site
        - The SharePoint site retrieved has the correct url
        """
        # execution
        fiscal = client.get_fiscal_site()
        # validation
        assert isinstance(fiscal, FiscalSite)
        assert isinstance(fiscal.site, Site)
        assert "Fiscal" in fiscal.site.web_url

    def test_get_aging_report(self, client):
        """Tests that Client.get_aging_report() returns an AgingReportList instance

        Validates the following conditions:
        - The response returned is an instance of AgingReportList
        - AgingReportList.list exists and is an instance of O365.SharepointList
        - The SharePoint list retrieved has the correct name
        """
        # execution
        report = client.get_aging_report()
        # validation
        assert isinstance(report, AgingReportList)
        assert isinstance(report.list, SharepointList)
        assert report.list.name == "Priority Vendor Aging"


class TestAgingReportList:
    """Tests the AgingReportList methods that make calls to the Graph API"""

    def test_get_invoices(self, report):
        """Tests that the get_invoices() method executes correctly

        Validates the following conditions:
        - The response returned is dictionary of AgingReportItem instances
        - The correct set of invoices are returned
        - The response matches the value of AgingReportList.invoices
        """
        # execution
        invoices = report.get_invoices()
        print(invoices[0].fields)
        # validation
        assert len(invoices) == 3
        assert isinstance(invoices[0], AgingReportItem)
        assert invoices == report.invoices
