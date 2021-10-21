import os
from pathlib import Path

import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from dgs_fiscal.config import settings
from dgs_fiscal.systems.sharepoint import SharePoint
from dgs_fiscal.systems.core_integrator.driver import Driver
from dgs_fiscal.systems.citibuy import CitiBuy, models
from tests.utils.populate_citibuy_db import populate_db

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
    """Creates an instance of the CitiBuy class for integration testing"""
    return CitiBuy()


@pytest.fixture(scope="session", name="mock_db")
def fixture_citibuy_db(test_archive_dir):
    """Creates a local version of the CitiBuy database for testing"""
    db_path = test_archive_dir / "mock.db"
    db_path.touch(exist_ok=True)
    if os.name == "nt":  # Checks if OS is Windows
        conn_url = f"sqlite:///{db_path}"
    else:
        conn_url = f"sqlite:////{db_path}"
    engine = sqlalchemy.create_engine(conn_url)
    models.Base.metadata.create_all(engine)
    with Session(engine) as session:
        populate_db(session)
    return conn_url


@pytest.fixture(scope="session", name="mock_citibuy")
def fixture_mock_citibuy(mock_db):
    """Creates a mock instance of CitiBuy class for unit testing"""
    return CitiBuy(conn_url=mock_db)
