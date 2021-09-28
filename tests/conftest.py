import os
from pathlib import Path

import pytest

from aging_report.config import settings
from aging_report.sharepoint import SharePoint
from aging_report.core_integrator.driver import Driver
from aging_report.citibuy import CitiBuy

collect_ignore = ["integration_tests"]


@pytest.fixture(scope="session")
def test_config():
    """Returns the configuration settings for use in tests"""
    test_settings = settings.from_env("testing")
    return test_settings


@pytest.fixture(scope="session", name="test_sharepoint")
def fixture_test_sharepoint():
    """Creates an authenticated Graph API client for use in integration tests"""
    return SharePoint()


@pytest.fixture(scope="session", name="test_report")
def fixture_report(test_sharepoint):
    """Creates an instance of AgingReportList for use in integration tests"""
    return test_sharepoint.get_aging_report()


@pytest.fixture(scope="session", name="test_archive_dir")
def fixture_archive_dir(tmp_path_factory):
    """Sets up a temporary archive directory for testing"""
    basetemp = Path.cwd() / "archives" / "tests"
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(basetemp)
    basetemp.mkdir(parents=True, exist_ok=True)
    archive_dir = tmp_path_factory.mktemp("archives", numbered=False)
    return archive_dir


@pytest.fixture(scope="session", name="test_archive")
def fixture_archive(test_sharepoint, test_archive_dir):
    """Creates an instance of ArchiveFolder for use in integration tests"""
    return test_sharepoint.get_archive_folder(test_archive_dir)


@pytest.fixture(scope="module", name="driver")
def fixture_driver(test_archive_dir):
    """Creates a webdriver for testing"""
    download_dir = test_archive_dir / "core_integrator"
    driver = Driver(download_dir)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", name="test_citibuy")
def fixture_citibuy():
    """Creates an instance of the CitiBuy class for testing"""
    return CitiBuy()
