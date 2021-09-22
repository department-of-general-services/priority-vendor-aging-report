from __future__ import annotations  # prevents NameError for typehints
from pathlib import Path

from dynaconf import Dynaconf
from O365 import Account
from O365.drive import Drive
from O365.sharepoint import Site, Sharepoint, SharepointList

from aging_report.config import settings
from aging_report.sharepoint.aging_report import AgingReportList
from aging_report.sharepoint.archive import ArchiveFolder
from aging_report.sharepoint.utils import authenticate_account


class Client:
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
        self.aging_report: AgingReportList = None
        self.archive: ArchiveFolder = None

    @property
    def is_authenticated(self) -> bool:
        """Returns True if account is authenticated"""
        return self.account.is_authenticated

    def get_aging_report(self) -> AgingReportList:
        """Returns AgingReportList instance and stores it in self.aging_report"""
        report_id = self.config.report_id
        site_list = self.get_list_by_id(report_id)
        self.aging_report = AgingReportList(site_list)
        return self.aging_report

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

    def get_list_by_id(self, list_id: str) -> SharepointList:
        """Find and return SharepointList instance by the list_id

        Parameters
        ----------
        list_id: str
            The id of the SharePoint list to query

        Returns
        -------
        SharepointList
            An instance of the O365.SharepointList class for the SharePoint
            list that matches the list_id
        """
        site = self.site
        # query the endpoint
        url = site.build_url(f"/lists/{list_id}")
        response = site.con.get(url)
        response.raise_for_status()
        # convert the response into a SharepointList instance
        # syntax borrowed from O365.Site.get_list_by_name()
        site_list = site.list_constructor(
            parent=site,
            **{site._cloud_data_key: response.json()},  # pylint: disable=W0212
        )
        return site_list
