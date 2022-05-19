from pathlib import Path

import pytest
import pandas as pd

from dgs_fiscal.etl import PromptPayment
from dgs_fiscal.etl.prompt_payment.main import constants, ReportOutput
from dgs_fiscal.systems import CoreIntegrator, SharePoint

TEST_DIR = Path(__file__).parent.resolve()


@pytest.fixture(scope="session", name="test_prompt")
def fixture_prompt_payment(test_archive_dir):
    """Creates a fixture of the PromptPayment class for testing"""
    return PromptPayment(local_archive=test_archive_dir)


def new_report_file():
    """Returns the link to a dummy version of the report scraped from
    CoreIntegrator by CoreIntegrator.scrape_report()
    """
    current_dir = Path(__file__).parent
    return current_dir / "new_report_input.xlsx"


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

    def test_get_old_excel(self, test_prompt, test_archive, test_archive_dir):
        """Tests that the get_old_excel() method executes successfully

        Validates the following conditions:
        - A dataframe is returned as the result
        - The columns have been renamed correctly
        - The
        """
        # setup - reset mock AgingReport.xslx
        columns = list(constants.OLD_REPORT["dtypes"].keys())
        file_name = "PromptPaymentReport.xlsx"
        mock_file = TEST_DIR / "old_report_input.xlsx"
        upload = test_archive.upload_file(
            local_path=mock_file,
            folder_name="test",
            file_name=file_name,
        )
        assert upload.name == file_name
        # execution
        report_path = (
            "/Prompt Payment/Workflow Archives/test/PromptPaymentReport.xlsx"
        )
        output = test_prompt.get_old_excel(
            report_path=report_path,
            download_loc=test_archive_dir,
        )
        print(output.df.columns)
        print(output.df)
        # validation
        assert isinstance(output, ReportOutput)
        assert list(output.df.columns) == columns
        assert output.file.exists()

    def test_get_new_report(self, test_prompt, monkeypatch):
        """Tests that the get_new_report() method executes successfully

        Validates the following conditions:
        - A dataframe is returned as the result
        - The columns have been renamed correctly
        - There are no invoices on the list where the PromptPaymentReport
          field is False
        """
        # setup
        columns = list(constants.NEW_REPORT["columns"].values())
        monkeypatch.setattr(
            test_prompt.core_integrator,
            "scrape_report",
            new_report_file,
        )
        vendor_ids = ["00048571", "00048571", "00001928", "01012092"]
        # execution
        output = test_prompt.get_new_report()
        df = output.df
        # validation
        assert isinstance(output, ReportOutput)
        assert list(df.columns) == columns
        assert list(df["Vendor ID"]) == vendor_ids

    def test_reconcile_reports(self, test_prompt, test_archive_dir):
        """Tests that reconcile_reports() executes correctly

        Validates the following conditions
        """
        # setup
        dropped = ["37010778", "BCB4-33"]
        added = ["1851"]
        old_dtypes = constants.OLD_REPORT["dtypes"]
        new_dtypes = constants.NEW_REPORT["dtypes"]
        old_report = pd.read_excel(
            TEST_DIR / "old_report_output.xlsx",
            dtype=old_dtypes,
        )
        new_report = pd.read_excel(
            TEST_DIR / "new_report_output.xlsx",
            dtype=new_dtypes,
        )
        print(old_report)
        print(new_report)
        # execution
        output = test_prompt.reconcile_reports(
            new_report,
            old_report,
            test_archive_dir,
        )
        # validation
        for invoice in dropped:
            assert invoice not in list(output.df["Document Number"])
        for invoice in added:
            assert invoice in list(output.df["Document Number"])
