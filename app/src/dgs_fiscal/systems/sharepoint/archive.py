from pathlib import Path

import pandas as pd
from O365.drive import Folder, File


class ArchiveFolder:
    """Creates an API client for the Archive folder in the DGS Fiscal site

    Attributes
    ----------
    folder: Folder
        An instance of O365.Folder for the Archive folder in SharePoint
    archive_dir: Path
        The path to the local archive directory
    tmp_dir: Path
        A temporary directory in the archive directory used for downloading and
        manipulating files
    sub_folders: List[Folder]
        A list of instances of O365.Folder for each sub-folder in the Archive
    """

    def __init__(self, folder: Folder, archive_dir: Path = None) -> None:
        """Inits the Archive class"""
        self.folder = folder
        self.archive_dir = archive_dir or (Path.cwd() / "archives")
        self.tmp_dir = self.archive_dir / "tmp"
        self.subfolders = list(self.folder.get_child_folders())
        self.tmp_dir.mkdir(exist_ok=True, parents=True)

    def export_dataframe(
        self,
        df: pd.DataFrame,
        file_name: str,
    ) -> Path:
        """Export dataframe to Excel in local archive for upload to SharePoint
        and styles the data as a table

        Parameters
        ----------
        df: pd.DataFrame
            The dataframe to export to Excel
        file_name: str
            File name to save to save the exported dataframe under

        Returns
        -------
        Path
            Path to where the dataframe was saved as an Excel file
        """
        # set the export location to local tmp_dir
        file = self.tmp_dir / file_name

        # write the data to Excel and get the worksheet using XlsxWriter
        writer = pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            file, engine="xlsxwriter"
        )
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        worksheet = writer.sheets["Sheet1"]

        # format the data as a table and adjust col width
        (max_row, max_col) = df.shape
        columns = [{"header": column} for column in df.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": columns})
        worksheet.set_column(0, max_col - 1, 12)

        # save the file and return the path
        writer.save()
        return file

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
            What to name of the file once it"s uploaded
        """
        # check that the upload file exists
        if not local_path.exists():
            raise FileNotFoundError(f"No file found at {local_path}")
        # upload file
        folder = self.get_subfolder_by_name(folder_name)
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
            What to name the file when it"s downloaded. Default is to use the
            existing name of the file in SharePoint

        Returns
        -------
        Path
            Local path to where the downloaded file can be accessed
        """
        # make sure the download directory exists
        download_dir.mkdir(parents=True, exist_ok=True)
        # set the download path
        if download_name:
            download_path = download_dir / download_name
        else:
            download_path = download_dir / file.name
        file.download(download_dir, download_name)
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
        folder = self.get_subfolder_by_name(folder_name)
        files = folder.get_items()
        last_upload = next(files)
        for file in files:
            if file.created > last_upload.created:
                last_upload = file
        return last_upload

    def get_subfolder_by_name(self, name: str) -> Folder:
        """Returns an O365.Folder instance of the sub-folder that matches the
        name passed as a parameter
        """
        folder = next((f for f in self.subfolders if f.name == name), None)
        if not folder:
            raise KeyError(f"No sub-folder found with the name {name}")
        return folder

    def _clean_tmp_dir(self) -> None:
        """Removes any remaining files in self.tmp_dir"""
        for file in self.tmp_dir.iterdir():
            file.unlink()
