from pathlib import Path

import pandas as pd
from O365.drive import Folder, File


class ArchiveFolder:
    """Creates an API client for the Archive folder in the DGS Fiscal site"""

    def __init__(self, folder: Folder, archives_dir: Path = None) -> None:
        """Inits the Archive class"""
        archives_dir = archives_dir or (Path.cwd() / "archives")
        self.folder = folder
        self.tmp_dir = archives_dir / "tmp"
        self.subfolders = []

    def get_subfolders(self):
        """Gets sub-folders from the Archive folder in SharePoint and adds them
        to the self.subfolders attribute
        """
        self.subfolders = list(self.folder.get_child_folders())
        return self.subfolders

    def upload_file(
        self,
        local_path: Path,
        folder_name: str,
        file_name: str,
    ) -> None:
        """Uploads a file to a specific sub-folder in the Archive

        Parameters
        ----------
        local_path: Path
            Path to where the file to upload is stored locally
        folder_name: str
            Name of the sub-folder in the archive where the file will be
            uploaded. Must be one of the folders in self.subfolders
        file_name: str
            What to name of the file once it's uploaded
        """
        # check that the upload file exists
        if not local_path.exists():
            raise FileNotFoundError(f"No file found at {local_path}")
        # upload file
        folder = self._get_subfolder_by_name(folder_name)
        file = folder.upload_file(local_path, file_name)
        return file

    def download_file(
        self,
        file: File,
        download_dir: Path,
        download_name: str = None,
    ) -> Path:
        """Downloads a file from an archive sub-folder to a local directory

        Parameters
        ----------
        file: File
            Instance of O365.File to download
        download_path: Path
            Local path to where file will be downloaded
        download_name: str, optional
            What to name the file when it's downloaded. Default is to use the
            existing name of the file in SharePoint

        Returns
        -------
        Path
            Local path to where the downloaded file can be accessed
        """
        # make sure the download directory exists
        download_dir.makedir(parents=True, exist_ok=True)
        # set the download path
        if download_name:
            download_path = download_dir / download_name
        else:
            download_path = download_dir / file.name
        file.download(download_path)
        return download_path

    def read_excel(self, file: File) -> pd.DataFrame:
        """Downloads an excel file from SharePoint and loads it as a dataframe

        Parameters
        ----------
        file: File
            Instance of O365.File to read in as a dataframe
        file_name: str
            Name of the Excel file to read in as a dataframe

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of the file downloaded from SharePoint
        """
        pass

    def get_last_upload(self, folder_name: str) -> File:
        """Return the most recently created file in the Archive sub-folder that
        matches the folder_name parameter

        Parameters
        ----------
        folder_name: str
            Name of the sub-folder from which the most recent upload will be
            returned. Must be one of the folders in self.subfolders

        Returns
        -------
        File
            An instance of O365.File for the most recently created file
        """
        folder = self._get_subfolder_by_name(folder_name)
        files = folder.get_items()
        last_upload = next(files)
        for file in files:
            if file.created > last_upload.created:
                last_upload = file
        return last_upload

    def _clean_tmp_dir(self) -> None:
        """Removes any remaining files in self.tmp_dir"""
        for file in self.tmp_dir.iterdir():
            file.unlink()

    def _get_subfolder_by_name(self, name: str) -> Folder:
        """Returns an O365.Folder instance of the sub-folder that matches the
        name passed as a parameter
        """
        if not self.subfolders:
            self.get_subfolders()
        folder = next((f for f in self.subfolders if f.name == name), None)
        if not folder:
            raise KeyError(f"No sub-folder found with the name {name}")
        return folder
