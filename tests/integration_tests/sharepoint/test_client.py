from O365 import Account
from O365.sharepoint import Sharepoint, Site, SharepointList

from aging_report.sharepoint import FiscalSite, AgingReportList


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
