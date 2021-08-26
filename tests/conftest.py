import pytest
from O365 import Account

from aging_report.config import settings

collect_ignore = ["integration_tests"]


@pytest.fixture(scope="session")
def test_config():
    """Returns the configuration settings for use in tests"""
    test_settings = settings.from_env("testing")
    return test_settings


@pytest.fixture(scope="session")
def account():
    """Create an authenticated Graph API client for use in integration tests"""
    credentials = (settings.client_id, settings.client_secret)
    client = Account(
        credentials,
        auth_flow_type="credentials",
        tenant_id=settings.tenant_id,
    )
    client.authenticate()
    return client
