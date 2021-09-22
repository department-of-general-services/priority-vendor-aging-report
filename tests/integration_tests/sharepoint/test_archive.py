from pathlib import Path

from O365.drive import Folder, File

DATA_DIR = Path.cwd() / "tests" / "integration_tests" / "sharepoint" / "data"
TEST_FOLDER = "test"


class TestArchiveFolder:
    """Tests the ArchiveFolder class"""

    def test_get_subfolders(self, test_archive):
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
        folders = test_archive.get_subfolders()
        folder_names = [f.name for f in folders]
        print(folder_names)
        # validation
        assert isinstance(folders[0], Folder)
        assert folders == test_archive.subfolders
        assert folder_names == expected

    def test_upload_file(self, test_archive):
        """Tests that the ArchiveFolder.upload_file() method successfully
        uploads a file to the archive sub-folder specified.

        Validates the following conditions:
        - The result returned is an instance of O365.File
        - The name of that file matches the file_name passed to upload_file()
        """
        # setup
        file_loc = DATA_DIR / "upload.csv"
        file_name = "test_upload.csv"
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
        # execution
        output = test_archive.get_last_upload(TEST_FOLDER)
        # validation
        assert isinstance(output, File)
        assert output.name == "test_last_upload.csv"
