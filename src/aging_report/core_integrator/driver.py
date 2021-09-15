from __future__ import annotations  # prevents NameError for typehints
from pathlib import Path

from dynaconf import Dynaconf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Expected
from selenium.common.exceptions import (
    TimeoutException,
    SessionNotCreatedException,
)

from aging_report.config import settings


class Driver:
    """A Selenium webdriver used to operate a Chrome browser"""

    def __init__(
        self,
        download_dir: Path,
        config: Dynaconf = settings,
    ) -> None:
        """Inits the Driver class with specific download directory

        Parameters
        ----------
        download_dir: Path
            Path to directory where downloads from the browser should be saved
        driver_path: Path
            Location where the latest version of chromedriver is downloaded
        """
        # get path to chromedriver and project root
        self.driver_path = Path(config.chrome_driver_path)
        self.download_dir = download_dir
        self.driver = self.create_driver(self.download_dir, self.driver_path)

    def create_driver(
        self,
        download_dir: Path,
        driver_path: Path,
    ) -> webdriver.Chrome:
        """Configures a selenium webdriver with a specific download directory

        Parameters
        ----------
        driver_path: Path
            Location where the latest version of chromedriver is downloaded
        download_dir: Path
            Path to directory where downloads from the browser should be saved

        Returns
        -------
        webdriver.Chrome
            Selenium webdriver for Chrome with options configured
        """
        # sets default download directory
        download_dir.mkdir(exist_ok=True, parents=True)
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": str(download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)

        # creates driver
        if not driver_path.exists():
            message = f"No chromedriver found at '{driver_path}'"
            raise FileNotFoundError(message)
        try:
            driver = webdriver.Chrome(str(driver_path), options=options)
        except SessionNotCreatedException as error:
            raise error

        return driver

    def fill_in(self, element_id: str, content: str) -> None:
        """Uses the webdriver to fill in a form field with content

        Parameters
        ----------
        element_id: str
            Id attribute of the form field to fill in with data
        content: str
            The information with which to fill in the form field
        """
        return self.driver.find_element_by_id(element_id).send_keys(content)

    def click(self, locator: str, loc_type: str = "id") -> None:
        """Uses the webdriver to locate and click an element

        Parameters
        ----------
        locator: str
            Id or text of the HTML element used to locate and click it
        loc_type: str, optional
            The type of locator used to find the element to click. Default is
            to locate by id but also accepts "link" to locate by link text
        """
        if loc_type == "id":
            return self.driver.find_element_by_id(locator).click()
        if loc_type == "link":
            return self.driver.find_element_by_partial_link_text(
                locator
            ).click()
        raise KeyError("Parameter loc_type must be one of ('id','link')")

    def wait_to_load(
        self,
        locator: str,
        loc_type: str = "id",
        seconds: int = 45,
    ) -> None:
        """Forces the webdriver to wait until an element loads

        Parameters
        ----------
        locator: str
            Id or text of the HTML element used to check that it's loaded
        loc_type: str, optional
            The type of locator used to find the element to click. Default is
            to locate by id but also accepts "link" to locate by link text
        seconds: int, optional
            Time to wait for an element to load before raising an error
        """
        # set the locator type
        if loc_type == "id":
            by = By.ID
        elif loc_type == "link":
            by = By.PARTIAL_LINK_TEXT
        else:
            raise KeyError("Parameter loc_type must be one of ('id','link')")

        # try to locate the element within the given number of seconds
        try:
            elem_present = Expected.presence_of_element_located((by, locator))
            WebDriverWait(self.driver, seconds).until(elem_present)
        except TimeoutException as error:
            raise error

    def get(self, url) -> None:
        """Loads the webpage for a URL"""
        return self.driver.get(url)

    def quit(self) -> None:
        """Closes the webdriver"""
        return self.driver.quit()

    @property
    def current_url(self) -> str:
        """Returns the URL that the webdriver is currently on"""
        return self.driver.current_url
