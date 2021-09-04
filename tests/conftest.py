import pytest

from aging_report.config import settings
from aging_report.sharepoint import Client

collect_ignore = ["integration_tests"]


@pytest.fixture(scope="session")
def test_config():
    """Returns the configuration settings for use in tests"""
    test_settings = settings.from_env("testing")
    return test_settings


@pytest.fixture(scope="session", name="test_client")
def fixture_test_client():
    """Create an authenticated Graph API client for use in integration tests"""
    return Client()


@pytest.fixture(scope="session", name="test_report")
def fixture_report(test_client):
    """Create an instance of AgingReportList for use in integration tests"""
    return test_client.get_aging_report()
