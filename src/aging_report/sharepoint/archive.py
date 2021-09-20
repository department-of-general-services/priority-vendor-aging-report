from pathlib import Path

from O365.drive import DriveItem, Folder, File


class ArchiveFolder:
    """Creates an API client for the Archive folder in the DGS Fiscal site"""

    def __init__(self, folder: Folder):
        """Inits the Archive class"""
        self.folder = folder
        self.sub_folders = {}

    def get_sub_folders(self):
        """Gets sub-folders from the Archive folder in SharePoint and adds them
        to the self.sub_folders attribute
        """

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
            uploaded. Must be one of the folders in self.sub_folders
        file_name: str
            What to name of the file once it's uploaded
        """
