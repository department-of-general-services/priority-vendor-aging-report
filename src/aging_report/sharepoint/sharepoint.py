import msal
import requests

from aging_report.config import settings


class SharePoint:
    def __init__(self, config=settings):

        self.scopes = config.scopes
        self.session = None

        try:
            self.app = msal.ConfidentialClientApplication(
                config.client_id,
                authority=config.authority,
                client_credential=config.client_secret,
            )
        except AttributeError as err:
            print("One of the config variables isn't set")
            raise err

    def authenticate(self):

        result = self.app.acquire_token_silent(self.scopes, account=None)
        if not result:
            result = self.app.acquire_token_for_client(self.scopes)
        if "access_token" not in result:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))
