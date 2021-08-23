import pytest
import requests

from aging_report.config import settings
from aging_report.sharepoint import SharePoint, Site


class TestSharePoint:
    @pytest.mark.skip
    def test_authenticate_success(self):
        client = SharePoint()
        token = client.authenticate()
        assert token is not None

    def test_authenticate_wrapper(self):
        # setup
        site = Site(settings.site_id)
        # execution
        response = site.get_site()
        data = response.json()
        print(data)
        # validation
        assert response.status_code == 200
        assert "displayName" in data
        assert 0
