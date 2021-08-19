import msal

from aging_report.config import settings
from aging_report.sharepoint import SharePoint


class TestGraph:
    def test_authenticate_success(self):
        client = SharePoint()
        client.authenticate()
        result = client.app.acquire_token_silent(settings.scopes, account=None)
        assert "access_token" in result
