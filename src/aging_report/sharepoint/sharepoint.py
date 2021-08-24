import functools

import requests
from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import (
    ClientSecretCredential,
    CredentialUnavailableError,
)

from aging_report.config import settings


def authenticate_request(func):
    """Wrap each request in a session object that has the access token
    set as a header to ensure that the request is authenticated
    """

    @functools.wraps(func)
    def create_session_with_token(self, *args, **kwargs):
        # gets an access token
        access_token = self.client.authenticate()
        headers = {"Authorization": "Bearer " + access_token.token}
        # create a session object and set headers
        with requests.Session() as session:
            session.headers.update(headers)
            return func(self, session, *args, **kwargs)

    return create_session_with_token


class SharePoint:
    """Creates a client to interface with SharePoint using Microsoft Graph API
    and the Azure identity package from the Azure SDK for Python
    """

    def __init__(self, config=settings):
        """Inits the SharePoint class with specific config settings"""
        self.scopes = config.scopes
        try:
            # instantiate a daemon app for authentication with azure identity
            self.client = ClientSecretCredential(
                config.tenant_id,
                config.client_id,
                config.client_secret,
            )
        except AttributeError as err:
            print("One of the config variables isn't set")
            raise err

    def authenticate(self) -> AccessToken:
        """Find a cached access token or request a new one and return it"""
        try:
            token = self.client.get_token(self.scopes)
        except (CredentialUnavailableError, ClientAuthenticationError) as err:
            raise err
        return token


class Site:
    """Provides a wrapper for making calls to the Site resource in Graph API"""

    def __init__(self, client, site_id):
        """Inits the Site class for a particular SharePoint site"""
        self.client = client
        self.site_id = site_id
        self.site_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}"

    @authenticate_request
    def get_site_details(self, session):
        """Makes a call to GET /sites/{site_id}"""
        return session.get(self.site_url)

    @authenticate_request
    def get_lists(self, session):
        """Makes a call to GET /sites/{site_id}/list"""
        url = self.site_url + "/lists"
        return session.get(url)


class SiteList:
    """Provides a wrapper for making calls to the List resource in Graph API"""

    def __init__(self, client, site, list_id):
        """Inits the SiteList class for a particular SharePoint list"""
        self.client = client
        self.list = site
        self.list_id = list_id

    @authenticate_request
    def get_list_details(self, session):
        """Makes a call to GET lists/{list_id}"""
        pass
