def test_config_fixture(test_config):
    """Tests that all of the testing env config variables are set correctly
    when using the test_config fixture from conftest

    Tests the following conditions:
    - current_env is "testing"
    - The following variables all match the values set in settings.toml
      - client_id
      - client_secret
      - scopes
      - tenant_id
      - host_name
      - site_name
    """
    assert test_config.current_env == "testing"
    assert test_config.client_id == "test_id"
    assert test_config.client_secret == "test_secret"
    assert test_config.scopes == "https://graph.microsoft.com/.default"
    assert test_config.tenant_id == "12345"
    assert test_config.site_id == "acme.sharepoint.com,12345,67890"
    assert test_config.host_name == "acme.sharepoint.com"
    assert test_config.site_name == "AcmeSite"
