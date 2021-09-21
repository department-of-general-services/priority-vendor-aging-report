from pathlib import Path

from O365.drive import Folder


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
        download_path: Path,
        folder_name: str,
        file_name: str,
    ) -> None:
        """Downloads a file from an archive sub-folder to a local directory

        Parameters
        ----------
        download_path: Path
            Path to local directory where file will be downloaded
        folder_name: str
            Name of the sub-folder to search for the file by name. Must be the
            name of a folder in self.subfolders
        file_name: str,
            Name of the file to download
        """
        pass

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
