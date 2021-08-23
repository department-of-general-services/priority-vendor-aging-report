import functools

import requests
from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import (
    ClientSecretCredential,
    CredentialUnavailableError,
)

from aging_report.config import settings


class SharePoint:
    """Creates a client to interface with SharePoint using Microsoft Graph API
    and the Microsoft Authentication Library (MSAL)
    """

    def __init__(self, config=settings):

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


class Site(SharePoint):
    def __init__(self, site_id):
        super().__init__()
        self.site_id = site_id

    def get_site(self):

        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}"

        token = super().authenticate()
        headers = {"Authorization": "Bearer " + token.token}

        with requests.Session() as session:
            session.headers.update(headers)
            return session.get(url)
