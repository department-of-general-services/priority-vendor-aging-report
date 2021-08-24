import pytest
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import CredentialUnavailableError

from aging_report.sharepoint import SharePoint
from aging_report.config import settings


class TestSharePoint:
    """Unit tests for the SharePoint class"""

    def test_init_missing_creds(self):
        """Tests that __init__() fails correctly if config variables aren't set

        Tests the following condition:
        - __init__() raises an AttributeError when one of the config variables
          is missing
        """
        # setup
        config = settings.from_env("default")
        assert config.get("client_id") is None
        # execution
        with pytest.raises(AttributeError):
            SharePoint(config=config)

    def test_auth_client_authentication_error(self, test_config):
        """Tests that authenticate() fails correctly if the scope is incorrect

        Tests the following condition:
        - authenticate() raises a ClientAuthenticationError when the tenant_id
          is passed incorrectly
        """
        # setup
        assert test_config.tenant_id == "12345"
        # execution
        with pytest.raises(ClientAuthenticationError):
            client = SharePoint(test_config)
            client.authenticate()

    def test_auth_credential_unavailable_error(self):
        """Tests that authenticate() fails correctly if one of the credentials
        are missing

        - authenticate() raises a CredentialUnavailableError if one of the
          credentials are missing
        """
        # TODO: implement this
        assert 1
