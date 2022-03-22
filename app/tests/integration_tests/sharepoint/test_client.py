import pytest
from O365 import Account
from O365.drive import Folder
from O365.sharepoint import Sharepoint, Site, SharepointList

from dgs_fiscal.systems.sharepoint.list import SiteList
from dgs_fiscal.systems.sharepoint.archive import ArchiveFolder


class TestClient:
    """Tests the Client methods that make external calls to Graph API"""

    def test_init(self, test_sharepoint):
        """Tests that Client instantiates correctly

        Validatees the following conditions:
        - Client.account exists and is an instance of O365.Account
        - Client.app exists and is an instance of O365.Sharepoint
        - DGSFiscal.site exists and is an instance of O365.Site
        - The SharePoint site retrieved has the correct url
        - Client.account is authenticated with Graph API
        """
        # validation
        assert isinstance(test_sharepoint.account, Account)
        assert isinstance(test_sharepoint.app, Sharepoint)
        assert isinstance(test_sharepoint.site, Site)
        assert "Fiscal" in test_sharepoint.site.web_url
        assert test_sharepoint.is_authenticated

    @pytest.mark.parametrize(
        "list_name",
        ["Vendors", "PO Releases", "Invoices", "Master Blanket POs"],
    )
    def test_get_list(self, test_sharepoint, list_name):
        """Tests that Client.get_vendor_list() returns an SiteList instance

        Validates the following conditions:
        - The response returned is an instance of SiteList
        - SiteList.list exists and is an instance of O365.SharepointList
        - The SharePoint list retrieved has the correct name
        """
        # execution
        sp_list = test_sharepoint.get_list(list_name)
        # validation
        assert isinstance(sp_list, SiteList)
        assert isinstance(sp_list.list, SharepointList)
        assert sp_list.list.name is not None

    def test_get_archive_folder(self, test_sharepoint, test_archive_dir):
        """Tests that Client.get_archive_folder() returns an ArchiveFolder instance

        Validates the following conditions:
        - The response returned is an instance of ArchiveFolder
        - ArchiveFolder.list exists and is an instance of O365.Folder
        - The folder has the right name
        - ArchiveFolder.tmp_dir points to the correct local directory and that
          directory exists
        """
        # setup
        tmp_dir = test_archive_dir / "tmp"
        # execution
        archive = test_sharepoint.get_archive_folder(test_archive_dir)
        # validation
        assert isinstance(archive, ArchiveFolder)
        assert isinstance(archive.folder, Folder)
        assert archive.folder.name == "Workflow Archives"
        assert archive.tmp_dir == tmp_dir

    def test_get_folder_by_path(self, test_sharepoint):
        """Tests get_folder_by_path() method"""
        # setup
        path = "/Prompt Payment"
        # execution
        folder = test_sharepoint.get_folder_by_path(path)
        # validation
        assert folder.name == "Prompt Payment"
