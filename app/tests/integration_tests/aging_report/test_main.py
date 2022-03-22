from datetime import datetime
from pathlib import Path

import pytest
import pandas as pd

from dgs_fiscal.etl import AgingReport
from dgs_fiscal.systems import SharePoint
from dgs_fiscal.etl.aging_report import constants


@pytest.fixture(scope="session", name="mock_aging")
def fixture_aging_report(mock_db):
    """Mocks the ContractManagement class with the local CitiBuy db"""
    return AgingReport(citibuy_url=mock_db)


class TestAgingReport:
    """Tests the AgingReport class"""

    def test_init(self, mock_aging):
        """Tests that AgingReport class inits correctly

        Validates the following conditions:
        - The AgingReport class was instantiated with the mock_db
        - AgingReport.sharepoint is an instance of the SharePoint class
        """
        # execution
        records = mock_aging.citibuy.get_purchase_orders().records
        # validation
        assert len(records) == 7
        assert isinstance(mock_aging.sharepoint, SharePoint)

    def test_get_citibuy_data(self, mock_aging):
        """Tests that the get_citibuy_data() method executes correctly

        Validates the following conditions:
        - The correct set of invoices are returned from CitiBuy
        - Each record has all of the necessary fields
        """
        # setup
        cols = list(constants.CITIBUY["invoice_cols"].values())
        # execution
        output = mock_aging.get_citibuy_data()
        print(output)
        # validation
        assert list(output.columns) == cols
        for val in output["Invoice Status"]:
            assert val in mock_aging.citibuy.INVOICE_STATUS.values()
        for val in output["PO Status"]:
            assert val in mock_aging.citibuy.PO_STATUS.values()

    def test_upload_invoice_data(self, mock_aging, test_archive_dir):
        """Tests that upload_invoice_data() method executes correctly

        Validates the following conditions:
        - The file has been uploaded to SharePoint
        - The filename that is uploaded contains today's date
        """
        # setup
        date_str = datetime.today().strftime("%Y-%m-%d")
        file_name = f"{date_str}_InvoiceExport.xlsx"
        df = pd.DataFrame({"Col A": ["a", "b"], "Col B": ["d", "f"]})
        # execution
        file = mock_aging.upload_invoice_data(
            df=df,
            folder_name="test",
            local_archive=test_archive_dir,
        )
        # validation
        assert file.name == file_name


class TestGetSharePointData:
    """Tests the AgingReport.get_sharepoint_data() method"""

    def test_get_sharepoint_data(
        self, mock_aging, test_archive, test_archive_dir
    ):
        """Tests that the get_sharepoint_data() method executes correctly

        Validates the following conditions:
        - get_sharepoint_data() returns a dataframe of the blank Aging Report
          downloaded from SharePoint
        - The resulting dataframe reads the vendor ID in as a string
        """
        # setup - reset mock AgingReport.xslx
        curr_dir = Path(__file__).parent.resolve()
        mock_file = curr_dir / "SampleAgingReport.xlsx"
        expected = pd.read_excel(mock_file)
        upload = test_archive.upload_file(
            local_path=mock_file,
            folder_name="test",
            file_name="AgingReport.xlsx",
        )
        assert upload.name == "AgingReport.xlsx"
        # execution
        report_path = "/Prompt Payment/Workflow Archives/test/AgingReport.xlsx"
        df = mock_aging.get_sharepoint_data(
            report_path=report_path,
            download_loc=test_archive_dir,
        )
        print(df)
        # validation
        assert df.shape == expected.shape
        assert df.loc[0, "Vendor ID"] == "111"
