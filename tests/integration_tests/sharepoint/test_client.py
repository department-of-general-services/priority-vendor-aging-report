from O365 import Account
from O365.drive import Folder
from O365.sharepoint import Sharepoint, Site, SharepointList

from aging_report.sharepoint import BaseList, ArchiveFolder


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

    def test_get_aging_report(self, test_sharepoint):
        """Tests that Client.get_aging_report() returns an BaseList instance

        Validates the following conditions:
        - The response returned is an instance of BaseList
        - BaseList.list exists and is an instance of O365.SharepointList
        - The SharePoint list retrieved has the correct name
        """
        # execution
        report = test_sharepoint.get_aging_report()
        # validation
        assert isinstance(report, BaseList)
        assert isinstance(report.list, SharepointList)
        assert report.list.name == "Priority Vendor Aging"

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
