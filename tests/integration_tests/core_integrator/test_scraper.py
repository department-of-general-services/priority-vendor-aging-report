import faulthandler

import pandas as pd

from aging_report.core_integrator.scraper import CoreIntegrator


def test_scraper(test_archive_dir):
    """Tests that CoreIntegrator.scrape_report() executes correctly

    Validates the following conditions:
    - The method doesn't raise any errors
    - The report was downloaded to the archives directory
    - It returns a dataframe
    - The values in the Execution ID column are populated
    """
    # setup
    faulthandler.disable()
    scraper = CoreIntegrator(test_archive_dir)
    # execution
    df = scraper.scrape_report(attempts=2)
    print(df.head())
    faulthandler.enable()
    # validation
    assert scraper.file_path.exists()
    assert isinstance(df, pd.DataFrame)
    assert all(pd.notna(df["Execution ID"]))
