from __future__ import annotations  # prevents NameError for typehints
import time
from datetime import date
from pathlib import Path

import pandas as pd
import xlwings as xl
from dynaconf import Dynaconf
from selenium.common.exceptions import (
    TimeoutException,
    UnexpectedAlertPresentException,
    SessionNotCreatedException,
)

from aging_report.config import settings
from aging_report.core_integrator.driver import Driver
from aging_report.core_integrator.constants import CORE_ELEMENTS


class CoreIntegrator:
    """Client for scraping reports from the CoreIntegrator website

    Attributes
    ----------
    elements: dict
        Dictionary of HTML id tags used to select elements on the CoreIntegrator
        website with the Selenium webdriver
    download_dir: Path
        Path to the directory where the report scraped from CoreIntegrator will
        be donwloaded
    download_path: Path
        Path to the location of the report that's downloaded from CoreIntegrator
    file_path: Path
        Path to location of the report after it's been renamed with today's date
    driver: Driver
        Instance of Driver class used to programmatically interact with the
        CoreIntegrator website and access the Prompt Payment Report
    """

    EXCEPTIONS = (
        KeyError,
        FileNotFoundError,
        TimeoutException,
        UnexpectedAlertPresentException,
        SessionNotCreatedException,
    )

    def __init__(  # pylint: disable=dangerous-default-value
        self,
        elements: dict = CORE_ELEMENTS,
        archives_dir: Path = None,
    ) -> None:
        """Inits the CoreIntegrator class"""
        # sets download directory and file names
        report_name = elements["report name"]
        archives_dir = archives_dir or (Path.cwd() / "archives")
        download_dir = archives_dir / "core_integrator"
        download_name = report_name + ".xlsx"
        file_name = f"prompt_payment{str(date.today())}.xlsx"
        # sets class attributes
        self.elements = elements
        self.download_dir = download_dir
        self.download_path = download_dir / download_name
        self.file_path = download_dir / file_name
        self.driver: Driver = None

    def scrape_report(self, config: Dynaconf = settings) -> pd.DataFrame:
        """Scrapes and downloads the Prompt Payment report from CoreIntegrator
        then loads it as a dataframe

        Parameters
        ----------
        config: Dynaconf
            The configuration settings that contain the path to the Selenium
            chromedriver executable and the user credentials for CoreIntegrator

        Returns
        -------
        pd.DataFrame
            The scraped Prompt Payment report loaded as a pandas dataframe
        """
        # try to scrape the report, up to 10 attempts
        for _ in range(10):
            try:
                self.driver = Driver(self.download_dir, config)
                self._login(config)
                self._access_report()
                self._rename_download()
                return self.load_report()
            except self.EXCEPTIONS as e:
                error = e
            finally:
                self.driver.quit()
        raise error

    def _login(self, config: Dynaconf) -> None:
        """Logs into the CoreIntegrator website to initiate scraping

        Parameters
        ----------
        config: Dynaconf
            Configuration settings that contain credentials to CoreIntegrator
        """
        # rename attributes and config vars for ease
        driver = self.driver
        elements = self.elements
        username_field = elements["username box"]
        password_field = elements["password box"]
        login_button = elements["login button"]

        # load CoreIntegrator site and enter credentials
        driver.get(config["url"])
        driver.wait_to_load(username_field, seconds=5)
        driver.fill_in(username_field, config["core_username"])
        driver.fill_in(password_field, config["core_password"])

        # click the login button
        try:
            driver.click(login_button)
        except UnexpectedAlertPresentException as error:
            raise error

    def _access_report(self):
        """Searches for the Prompt Payment Report current through today's
        date and then exports the report to Excel
        """
        # rename attributes and config vars for ease
        driver = self.driver
        elements = self.elements
        today = date.today().strftime("%m/%d/%Y")
        report_link = elements["report name"]
        date_field = elements["date box"]
        report_label = elements["report_label"]
        view_report = elements["view report"]
        export_report = elements["export report"]

        # click on the prompt payment link
        driver.wait_to_load(report_link, loc_type="link")
        driver.click(report_link, loc_type="link")

        # enter today's date in the search box
        driver.wait_to_load(date_field)
        driver.fill_in(date_field, today)
        driver.click(report_label)  # click out of date_field

        # click view report button
        driver.wait_to_load(view_report)
        driver.click(view_report)

        # export report
        driver.wait_to_load(export_report, seconds=90)
        driver.click(export_report)

        # accept the dialog box to tigger the download
        time.sleep(1)
        driver.driver.switch_to.alert.accept()

    def _rename_download(self, attempts: int = 60) -> None:
        """Confirms report was downloaded and renames it

        Parameters
        ----------
        attempts: int, optional
            Number of attempts to check for the downloaded report. Default is
            to attempt once per second for 60 seconds.
        """
        # set local vars for ease
        download_path = self.download_path
        renamed_path = self.file_path
        # try to locate the download for given number of attempts
        counter = 0
        while not download_path.exists():
            counter += 1
            time.sleep(1)
            if counter > attempts:
                message = (
                    f"File not found at '{download_path}' "
                    f"after {counter} seconds."
                )
                raise FileNotFoundError(message)
        # rename downloaded file
        download_path.replace(renamed_path)

    def load_report(self) -> pd.DataFrame:
        """Loads the downloaded report as a pandas dataframe

        Automates the opening and saving of an excel workbook before reading it
        in through pd.read_excel, which addresses the NaN issue described in
        this post: https://stackoverflow.com/a/41730454/7338319

        Returns
        -------
        pd.DataFrame
            The scraped Prompt Payment report loaded as a pandas dataframe
        """
        # check that the file exists
        file = self.file_path
        if not file.exists():
            raise FileNotFoundError(f"Report wasn't found at location: {file}")
        # open and save the wb to trigger formulas
        app = xl.App(visible=False)
        book = app.books.open(self.file_path)
        book.save()
        book.close()
        app.kill()
        # read the excel into a dataframe
        return pd.read_excel(file, engine="openpyxl")
