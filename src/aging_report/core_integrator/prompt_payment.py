from __future__ import annotations  # prevents NameError for typehints

import pandas as pd

from aging_report.core_integrator.scraper import CoreIntegrator


class PromptPayment:
    """Manages access to the Prompt Payment Report in CoreIntegrator, which
    serves as a data source for updates to the Aging Report in SharePoint

    Attributes
    ----------
    core_integrator: CoreIntegrator
        Instance of CoreIntegrator class used to scrape Prompt Payment Report
        from the CoreIntegrator website
    df: pd.DataFrame
        A dataframe of the current Prompt Payment Report l
    """

    def __init__(self) -> None:
        """Inits the PromptPayment class"""
        self.core_integrator = CoreIntegrator()
        self.df: pd.DataFrame = None

    def scrape(self) -> pd.DataFrame:
        """Downloads the current version of the Prompt Payment report from
        CoreIntegrator then loads as a pandas DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame of the Prompt Payment Report
        """
        pass

    def archive(self) -> None:
        """Uploads an archive of the current Prompt Payment Report to the
        Archives folder in the Fiscal SharePoint site
        """
        pass
