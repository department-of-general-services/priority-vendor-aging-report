import time
from pathlib import Path

import pytest
from selenium.common.exceptions import TimeoutException

from dgs_fiscal.systems.core_integrator.driver import Driver
from dgs_fiscal.config import settings

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
        # setup
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

    def test_missing_driver(self, test_archive_dir, monkeypatch):
        """Tests that create_driver() returns an error if the chromedriver
        file doesn't exist at the path specified in config.json
        """
        # setup
        driver_path = Path.cwd() / "fake"
        assert driver_path.exists() is False
        monkeypatch.setattr(settings, "chrome_driver_path", driver_path)
        # executive
        with pytest.raises(FileNotFoundError):
            Driver(test_archive_dir, config=settings)


class TestClick:
    """Tests the Driver.click() method"""

    def test_click_link(self, driver):
        """Tests that Driver.click() clicks the right html element when
        passed the partial text of the link to click
        """
        # setup
        url_out = "https://pypi.org/project/selenium/#description"
        link = "Project description"
        # execution
        driver.get(URL)
        driver.click(link, loc_type="link")
        # validation
        assert driver.current_url == url_out

    def test_click_id(self, driver):
        """Tests that Driver.click() clicks the right html element when
        passed the id of the link to click
        """
        # setup
        url_out = "https://pypi.org/project/selenium/#description"
        link_id = "description-tab"
        # execution
        driver.get(URL)
        driver.click(link_id)
        # validation
        assert driver.current_url == url_out

    def test_click_key_error(self, driver):
        """Tests that Driver.click() raises a KeyError when passed an invalid
        value for loc_type
        """
        # execution
        with pytest.raises(KeyError):
            driver.click("link_text", loc_type="text")


class TestFillIn:
    """Tests the Driver.fill_in() method"""

    def test_fill_in(self, driver):
        """Tests the Driver.fill_in() method"""
        # setup
        search_id = "search"
        value_in = "FooBar"
        # execution_id
        driver.get(URL)
        driver.fill_in(search_id, value_in)
        value_out = driver.driver.find_element_by_id(search_id).get_attribute(
            "value"
        )
        # validation
        assert value_in == value_out


class TestWaitToLoad:
    """Tests the Driver.wait_to_load() method"""

    def test_id_present(self, driver):
        """Tests that the driver successfully exits the wait_to_load() loop if
        an element with that id is loaded on the page
        """
        # setup
        search_id = "search"
        # execution
        driver.get(URL)
        driver.wait_to_load(search_id, seconds=2)
        search = driver.driver.find_element_by_id(search_id)
        # validation
        assert search is not None

    def test_link_present(self, driver):
        """Tests that the driver successfully exits the wait_to_load() loop if
        an element with that partial link text is loaded on the page
        """
        # setup
        link = "Project description"
        # execution
        driver.get(URL)
        driver.wait_to_load(link, loc_type="link", seconds=2)
        description = driver.driver.find_element_by_partial_link_text(link)
        # validation
        assert description is not None

    def test_id_missing(self, driver):
        """Tests that the wait_to_load() method raises an TimeoutException if
        the item with that id still isn't present after x number of seconds
        """
        # setup
        search_id = "fake_id"
        # execution
        driver.get(URL)
        with pytest.raises(TimeoutException):
            driver.wait_to_load(search_id, seconds=1)

    def test_link_missing(self, driver):
        """Tests that the wait_to_load() method raises an TimeoutException if
        the item with that link text isn't present after x number of seconds
        """
        # setup
        link = "fake_link"
        # execution
        driver.get(URL)
        with pytest.raises(TimeoutException):
            driver.wait_to_load(link, loc_type="link", seconds=1)
