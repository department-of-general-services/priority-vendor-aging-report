from __future__ import annotations  # prevents NameError for typehints

from dynaconf import Dynaconf
from O365 import Account
from O365.sharepoint import (
    Site,
    SharepointList,
)
from aging_report.config import settings


def authenticate_account(config: Dynaconf) -> Account:
    """Creates and authenticates an O365.Account instance

    Parameters
    ----------
    config: Dynaconf
        The config settings that will be used to authenticate the account with
        Microsoft Graph API

    Returns
    -------
    Account
        An instance of the Account class from O365 that has been authenticated
    """
    credentials = (config.client_id, config.client_secret)
    account = Account(
        credentials,
        auth_flow_type="credentials",
        tenant_id=config.tenant_id,
    )
    if not account.is_authenticated:
        account.authenticate()
    return account


class Client:
    """Creates a SharePoint client to manage Graph API access using O365"""

    def __init__(self, config: Dynaconf = settings):
        """Instantiates the Client class"""
        self.config = config
        self.account = authenticate_account(config)
        self.app = self.account.sharepoint()
        self.fiscal_site: DGSFiscalSite = None
        self.aging_report: AgingReportList = None

    @property
    def is_authenticated(self) -> bool:
        """Returns True if account is authenticated"""
        return self.account.is_authenticated

    def get_fiscal_site(self) -> DGSFiscalSite:
        """Returns DGSFiscalSite instance and stores it in self.fiscal_site"""
        site = self.app.get_site(self.config.site_id)
        self.fiscal_site = DGSFiscalSite(self, site)
        return self.fiscal_site

    def get_aging_report(self) -> AgingReportList:
        """Returns AgingReportList instance and stores it in self.aging_report"""
        site = self.fiscal_site or self.get_fiscal_site()
        site_list = site.get_list_by_id(self.config.report_id)
        self.aging_report = AgingReportList(self, site, site_list)
        return self.aging_report


class DGSFiscalSite:
    """Creates a SharePoint client for the DGS Fiscal site

    Facilitates accessing lists and drives in the DGS SharePoint site using
    the O365 library and the Microsoft Graph API.

    Attributes
    ----------
    client: Client
        An instance of the Client class to manage Graph API access
    site: Site
        An instance of O365.Site to
    """

    def __init__(self, client: Client, site: Site) -> None:
        """Instantiates the DGSFiscalSite class"""
        self.client = client
        self.site = site

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


class AgingReportList:
    """Creates an API client for the Priority Vendor Aging SharePoint list

    Facilitates reading/writing to the Priority Vendor Aging SharePoint list
    using the O365 library and the Microsoft Graph API.

    Attributes
    ----------
    client: Client
        An instance of the Client class to manage Graph API access
    site_list: O365.SharepointList
        An instance of the O365.SharepointList class that manages calls to the
        Lists resource in Graph API
    items: List[AgingReportItem]
        A list of the items in the PriorityVendorAging SharePoint list
        instantiated as members of the AgingReportItem class
    """

    def __init__(
        self,
        client: Client,
        site: DGSFiscalSite,
        site_list: SharepointList,
    ) -> None:
        """Instantiates the AgingReportList class

        Parameters
        ----------
        client: Client
            An instance of the client class to manage Graph API access
        site: DGSFiscalSite
            An instance of the DGSFiscalSite class that the Priority Vendor
            Aging list belongs to
        """
        self.client = client
        self.site = site
        self.list = site_list
        self.items = None

    def get_invoices(self) -> None:
        """Gets items from the Piority Vendor Aging list in SharePoint and
        instantiates them as members of the AgingReportItem class
        """
        pass

    def add_invoices(self, **kwargs) -> None:
        """Inserts a new item into the Priority Vendor Aging list in SharePoint
        and instantiates the result as a member of the AgingReportItem class
        """
        pass


class AgingReportItem:
    """Creates an API client for an item in the Priority Vendor Aging list

    Facilitates reading and updating items in the Priority Vendor Aging
    SharePoint list using the O365 library and the Microsoft Graph API.

    Attributes
    ----------

    """

    def __init__(self, **kwargs) -> None:
        """Instantiates the AgingReportItem class"""
        pass

    def update(self, **kwargs) -> None:
        """Updates the Priority Vendor Aging list item in SharePoint"""
        pass
