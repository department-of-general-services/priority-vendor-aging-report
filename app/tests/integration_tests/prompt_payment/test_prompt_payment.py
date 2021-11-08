import pytest
import pandas as pd

from dgs_fiscal.etl import PromptPayment
from dgs_fiscal.systems import CoreIntegrator, SharePoint


@pytest.fixture(scope="session", name="test_prompt")
def fixture_prompt_payment(test_archive_dir):
    """Creates a fixture of the PromptPayment class for testing"""
    return PromptPayment(local_archive=test_archive_dir)


class TestPromptPayment:
    """Tests the PromptPayment etl class"""

    def test_init(self, test_prompt, test_archive_dir):
        """Tests that the PromptPayment inits correctly"""
        # validation
        assert test_prompt.archive.archive_dir == test_archive_dir
        assert isinstance(test_prompt.core_integrator, CoreIntegrator)
        assert isinstance(test_prompt.sharepoint, SharePoint)

    def test_get_old_report(self, test_prompt):
        """Tests that the get_old_report() method executes successfully

        Validates the following conditions:
        - A dataframe is returned as the result
        - The columns have been renamed correctly
        - There are no invoices on the list where the PromptPaymentReport
          field is False
        """
        # execution
        df = test_prompt.get_old_report()
        print(df.columns)
        # validation
        assert isinstance(df, pd.DataFrame)
        assert len(df[~df["Prompt Payment"]]) == 0
