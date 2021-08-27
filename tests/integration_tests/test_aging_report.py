from pprint import pprint

import pytest
import requests
from O365 import Account
from O365.sharepoint import Sharepoint

from aging_report.config import settings
from aging_report.sharepoint import Client


class TestClient:
    def test_init(self, client):
        # validation
        assert isinstance(client.account, Account)
        assert isinstance(client.app, Sharepoint)
        assert client.is_authenticated

    def test_get_fiscal_site(self, client):
        # execution
        fiscal = client.get_fiscal_site()
        # validation
        assert fiscal.site
        assert "Fiscal" in fiscal.site.web_url

    def test_get_aging_report(self, client):
        # execution
        report = client.get_aging_report()
        # validation
        assert report
        assert report.list.name == "Priority Vendor Aging"
