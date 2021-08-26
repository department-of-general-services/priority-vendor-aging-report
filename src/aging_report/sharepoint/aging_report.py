# pylint: disable=unused-import
import requests
from O365 import Account
from O365.sharepoint import Sharepoint
from dynaconf import Dynaconf

from aging_report.config import settings


def authenticate_account(config: Dynaconf) -> Account:
    """Creates and authenticate an O365.Account instance"""
    credentials = (config.client_id, config.client_secret)
    client = Account(
        credentials,
        auth_flow_type="credentials",
        tenant_id=config.tenant_id,
    )
    client.authenticate()
    return client


class Client:
    """Creates a SharePoint client to manage Graph API access using O365"""

    def __init__(self, config: Dynaconf = settings):
        """Instantiates the Client class"""
        self.account = authenticate_account(config)
        self.client = self.account.sharepoint()

    @property
    def is_authenticated(self) -> bool:
        """Returns True if account is authenticated"""
        return self.account.is_authenticated


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

    def __init__(self, client: Client, config: Dynaconf = settings) -> None:
        """Instantiates the AgingReportList class

        Parameters
        ----------
        client: Client
            An instance of the client class to manage Graph API access
        config: Dynaconf, optional
            An instance of config settings that will be used to init this class.
            Default is to use the current config settings, but this allows the
            class to be instantiated with a test config instead.
        """

        self.client = client
        self.config = config
        self.site_list = None
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


    """

    def __init__(self, **kwargs) -> None:
        """Instantiates the AgingReportItem class"""
        pass

    def update(self, **kwargs) -> None:
        """Updates the Priority Vendor Aging list item in SharePoint"""
        pass
