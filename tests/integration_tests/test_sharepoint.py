from aging_report.config import settings
from aging_report.sharepoint import SharePoint


class TestGraph:
    def test_authenticate_success(self):
        client = SharePoint()
        token = client._authenticate()
        assert token is not None
