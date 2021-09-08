from __future__ import annotations  # prevents NameError for typehints


class CoreIntegrator:
    """Client for scraping data from the CoreIntegrator website"""

    def __init__(self):
        """Inits the CoreIntegrator class"""
        pass

    def scrape_report(self) -> None:
        """Scrapes and downloads the Prompt Payment report from CoreIntegrator
        then loads it as a dataframe
        """
        pass

    def _login(self):
        """Logs into the CoreIntegrator website"""
        pass

    def _access_report(self):
        """Searches for the Prompt Payment Report current through today's
        date and then exports the report to Excel
        """
        pass

    def _rename_download(self):
        """Confirms report was downloaded and renames it"""
        pass

    def _load_report(self):
        """Loads the report as a dataframe"""
        pass
