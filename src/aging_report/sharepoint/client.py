from __future__ import annotations  # prevents NameError for typehints
from pathlib import Path

from dynaconf import Dynaconf
from O365 import Account
from O365.drive import Drive
from O365.sharepoint import Site, Sharepoint

from aging_report.config import settings
from aging_report.sharepoint.list import SiteList
from aging_report.sharepoint.archive import ArchiveFolder
from aging_report.sharepoint.utils import authenticate_account


class SharePoint:
    """Creates a SharePoint client for the DGS Fiscal site

    Facilitates accessing lists and drives in the DGS SharePoint site using
    the O365 library and the Microsoft Graph API.

    Attributes
    ----------
    config: Dynaconf
        Configuration settings used to authenticate the client
    account: Account
        Instance of O365.Account that manages authentication with Graph API
    app: Sharepoint
        Instance of O365.Sharepoint that organizes other SharePoint classes
    site: Site
        An instance of the O365.Site class that manages calls to the Sites
        Graph API resource
    """

    def __init__(self, config: Dynaconf = settings):
        """Instantiates the Client class"""
        self.config: Dynaconf = config
        self.account: Account = authenticate_account(config)
        self.app: Sharepoint = self.account.sharepoint()
        self.site: Site = self.app.get_site(self.config.site_id)
        self.drive: Drive = None
        self.archive: ArchiveFolder = None

    @property
    def is_authenticated(self) -> bool:
        """Returns True if account is authenticated"""
        return self.account.is_authenticated

    def get_archive_folder(self, archive_dir: Path) -> ArchiveFolder:
        """Returns ArchiveFolder instance and stores it in self.archive

        Parameters
        ----------
        archive_dir: Path
            Path to local archive directory
        """
        drive_id = self.config.drive_id
        self.drive = self.site.get_document_library(drive_id)
        folder = self.drive.get_item(self.config.archive_id)
        self.archive = ArchiveFolder(folder, archive_dir)
        return self.archive

    def get_list(
        self,
        list_name: str,
        index_cols: list = None,
    ) -> SiteList:
        """Returns a SiteList instance for a SharePoint list specified by name

        Parameters
        ----------
        list_name: str
            The name of the list to return a SiteList instance for
        index_cols: list
            Columns that are indexed for querying data
        """
        site_list = self.site.get_list_by_name(list_name)
        return SiteList(site_list, key=index_cols)
