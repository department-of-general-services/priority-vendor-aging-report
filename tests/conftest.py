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
    credentials = (settings.client_id, settings.client_secret)
    account = Account(
        credentials,
        auth_flow_type="credentials",
        tenant_id=settings.tenant_id,
    )
    account.authenticate()
    return account
