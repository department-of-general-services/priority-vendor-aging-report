from pprint import pprint

import pytest
import requests

from aging_report.config import settings
from aging_report.sharepoint import SharePoint, Site


class TestSharePoint:
    """Tests the SharePoint class"""

    def test_authenticate_success(self):
        """Tests that the SharePoint.authenticate() method executes correctly

        Validates the following conditions:
        - The access token returned by authenticate() has the token attribute
        """
        client = SharePoint()
        access_token = client.authenticate()
        assert access_token.token


class TestSite:
    """Tests the Site class"""

    def test_get_site_details(self):
        """Tests that the Site.get_site_details() method executes correctly

        Validates the following conditions:
        - The response code is 200
        - The response has "displayName" in the data
        """
        # setup
        client = SharePoint()
        site = Site(client, settings.site_id)
        # execution
        response = site.get_site_details()
        data = response.json()
        print(data)
        # validation
        assert response.status_code == 200
        assert "displayName" in data

    def test_get_lists(self):
        """Tests that the Site.get_site_details() method executes correctly

        Validates the following conditions:
        - The response code is 200
        - The response has "displayName" in the data
        """
        # setup
        client = SharePoint()
        site = Site(client, settings.site_id)
        # execution
        response = site.get_lists()
        data = response.json()
        pprint(data["value"][0])
        # validation
        assert response.status_code == 200
        assert "value" in data
