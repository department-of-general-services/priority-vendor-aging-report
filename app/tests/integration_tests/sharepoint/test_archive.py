from pathlib import Path
from datetime import date

import pytest
import pandas as pd
from O365.drive import Folder, File

DATA_DIR = Path.cwd() / "tests" / "integration_tests" / "sharepoint" / "data"
TEST_FOLDER = "test"


class TestArchiveFolder:
    """Tests the ArchiveFolder class"""

    def test_init(self, test_archive):
        """Tests that the ArchiveFolder.get_subfolders() method returns the
        correct set of sub-folders and stores them in self.subfolders

        Validates the following conditions:
        - The self.subfolders method executes without any errors
        - It returns a list of O365.Folder instances
        - The returned value matches the list stored at self.subfolders
        - The names of the folders returned match the names of the sub-folders
          in the archive on SharePoint
        """
        # setup
        expected = [
            "aging_report",
            "commented_invoices",
            "core_integrator",
            "output",
            "test",
        ]
        # execution
        folders = test_archive.subfolders
        folder_names = [f.name for f in folders]
        print(folder_names)
        # validation
        assert isinstance(folders[0], Folder)
        assert folder_names == expected

    def test_get_sub_folder_error(self, test_archive):
        """Tests that the ArchiveFolder._get_subfolder_by_name() raises
        KeyError when passed a folder name that isn't in self.subfolders
        """
        # validation
        with pytest.raises(KeyError):
            test_archive.get_subfolder_by_name("fake")

    def test_upload_file(self, test_archive):
        """Tests that the ArchiveFolder.upload_file() method successfully
        uploads a file to the archive sub-folder specified.

        Validates the following conditions:
        - The result returned is an instance of O365.File
        - The name of that file matches the file_name passed to upload_file()
        """
        # setup
        file_loc = DATA_DIR / "upload.csv"
        date_str = date.today().strftime("%Y-%m-%d")
        file_name = f"test_upload_{date_str}.csv"
        # execution
        output = test_archive.upload_file(file_loc, TEST_FOLDER, file_name)
        # validation
        assert isinstance(output, File)
        assert output.name == file_name

    def test_get_last_upload(self, test_archive):
        """Tests that the ArchiveFolder.test_get_most_recent_archive() method
        successfully returns the most recent upload

        Validates the following conditions:
        - The result returned is an instance of O365.File
        - The name of that file matches the last uploaded csv
        """
        # setup
        date_str = date.today().strftime("%Y-%m-%d")
        # execution
        output = test_archive.get_last_upload(TEST_FOLDER)
        # validation
        assert isinstance(output, File)
        assert date_str in output.name

    def test_download_file(self, test_archive_dir, test_archive):
        """Tests that the ArchiveFolder.download_file() method successfully
        downloads a file to the location specified by download_path

        Validates the following conditions:
        - The result returned is an instance of Path
        - The Path returned is a file and it exists
        """
        # setup
        file_name = "test_download.csv"
        tmp_dir = test_archive_dir / "tmp"
        if tmp_dir.exists():
            for file in tmp_dir.iterdir():
                file.unlink()
            assert not any(tmp_dir.iterdir())
        file = test_archive.get_last_upload(TEST_FOLDER)
        # execution
        output = test_archive.download_file(file, tmp_dir, file_name)
        # validation
        assert isinstance(output, Path)
        assert output.name == file_name
        assert any(tmp_dir.iterdir())

    def test_export_dataframe(self, test_archive):
        """Tests that the export_dataframe() method successfully exports the
        dataframe to an Excel file and formats it with a table
        """
        # setup
        df = pd.DataFrame({"Col A": ["a", "b"], "Col B": ["d", "f"]})
        # execution
        file = test_archive.export_dataframe(df, "test.xlsx")
        # validation
        assert file.exists()
