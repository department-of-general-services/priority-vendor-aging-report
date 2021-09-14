import os
from pathlib import Path

import pytest

from aging_report.config import settings
from aging_report.sharepoint import Client
from aging_report.core_integrator.driver import Driver

collect_ignore = ["integration_tests"]


@pytest.fixture(scope="session")
def test_config():
    """Returns the configuration settings for use in tests"""
    test_settings = settings.from_env("testing")
    return test_settings


@pytest.fixture(scope="session", name="test_client")
def fixture_test_client():
    """Creates an authenticated Graph API client for use in integration tests"""
    return Client()


@pytest.fixture(scope="session", name="test_report")
def fixture_report(test_client):
    """Creates an instance of AgingReportList for use in integration tests"""
    return test_client.get_aging_report()


@pytest.fixture(scope="session", name="test_archive_dir")
def fixture_archive_dir(tmp_path_factory):
    """Sets up a temporary archive directory for testing"""
    basetemp = Path.cwd() / "archives" / "tests"
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(basetemp)
    basetemp.mkdir(parents=True, exist_ok=True)
    archive_dir = tmp_path_factory.mktemp("archives", numbered=False)
    return archive_dir


@pytest.fixture(scope="session", name="driver")
def fixture_driver(test_archive_dir):
    """Creates a webdriver for testing"""
    driver = Driver(test_archive_dir)
    yield driver
    driver.quit()
