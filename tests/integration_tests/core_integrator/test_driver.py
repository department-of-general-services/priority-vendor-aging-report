import time
from pathlib import Path

import pytest
from selenium.common.exceptions import (
    TimeoutException,
    SessionNotCreatedException,
)

from aging_report.core_integrator.driver import Driver
from aging_report.config import settings

URL = "https://pypi.org/project/selenium/#files"


class TestDriver:
    """Tests the Driver.__init__() method"""

    def test_success(self, driver, test_archive_dir):
        """Tests that __init__() executes successfully with the right inputs

        Validates the following conditions:
        - Driver is instantiated without raising an error
        - Driver.driver is an instance of webdriver.Chrome
        - And that it triggers a download to the specified directory
        """
        ## setup
        download_dir = test_archive_dir / "core_integrator"
        download_dir.mkdir(exist_ok=True, parents=True)
        assert not any(download_dir.iterdir())

        # execution
        try:
            driver.get(URL)
            driver.driver.implicitly_wait(5)
            driver.driver.find_element_by_partial_link_text("selenium").click()
            time.sleep(3)
        except Exception as err:
            raise err

        # validation
        assert isinstance(driver, Driver)
        assert any(download_dir.iterdir()) is True

    def test_missing_driver(self):
        """Tests that create_driver() returns an error if the chromedriver
        file doesn't exist at the path specified in config.json
        """
        # setup
        driver_path = Path.cwd() / "fake"
        assert driver_path.exists() is False
        settings.chrome_driver_path = driver_path

        # executive
        with pytest.raises(FileNotFoundError):
            Driver(config=settings)


@pytest.mark.skip
class TestClick:
    """Tests the Driver.click() method"""

    def test_click_link(self, driver):
        """ """
        # setup
        url_out = "https://pypi.org/project/selenium/#description"
        link = "Project description"

        # execution
        driver.get(URL)
        driver.click(driver, link, type="link")

        # validation
        assert driver.current_url == url_out
        driver.quit()

    def test_click_id(self, driver):
        # setup
        url_out = "https://pypi.org/project/selenium/#description"
        link_id = "description-tab"

        # execution
        driver.get(URL)
        driver.click(driver, link_id)

        # validation
        assert driver.current_url == url_out
        driver.quit()


@pytest.mark.skip
class TestFillIn:
    """Tests the Driver.fill_in() method"""

    def test_fill_in(self, driver):
        # setup
        search_id = "search"
        value_in = "FooBar"

        # execution_id
        driver.get(URL)
        driver.fill_in(driver, search_id, value_in)
        value_out = driver.find_element_by_id(search_id).get_attribute("value")

        # validation
        assert value_in == value_out
        driver.quit()


@pytest.mark.skip
class TestWaitToLoad:
    """Tests the Driver.wait_to_load() method"""

    def test_id_present(self, driver):
        # setup
        search_id = "search"
        # execution
        driver.get(URL)
        driver.wait_to_load(driver, search_id, seconds=2)
        search = driver.find_element_by_id(search_id)
        # validation
        assert search is not None
        driver.quit()

    def test_link_present(self, driver):
        # setup
        link = "Project description"

        # execution
        driver.get(URL)
        driver.wait_to_load(driver, link, type="link", seconds=2)
        description = driver.find_element_by_partial_link_text(link)

        # validation
        assert description is not None
        driver.quit()

    def test_id_missing(self, driver):
        # setup
        search_id = "fake_id"

        # execution
        driver.get(URL)
        with pytest.raises(TimeoutException):
            driver.wait_to_load(driver, search_id, seconds=1)
        driver.quit()

    def test_link_missing(self, driver):
        # setup
        link = "fake_link"

        # execution
        driver.get(URL)
        with pytest.raises(TimeoutException):
            driver.wait_to_load(driver, link, type="link", seconds=1)
        driver.quit()
