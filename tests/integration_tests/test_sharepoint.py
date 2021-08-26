from pprint import pprint

import pytest
import requests
from O365 import Account
from O365.sharepoint import Sharepoint

from aging_report.config import settings
from aging_report.sharepoint import Client


class TestClient:
    def test_init(self):
        # execution
        app = Client()
        # validation
        assert isinstance(app.account, Account)
        assert isinstance(app.client, Sharepoint)
        assert app.is_authenticated
