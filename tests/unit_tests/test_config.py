def test_config_fixture(test_config):
    """Tests that all of the testing env config variables are set correctly
    when using the test_config fixture from conftest

    Tests the following conditions:
    - username is not set
    - password is not set
    - base_url matches the CITIBUY_URL above
    """
    assert test_config.current_env == "testing"
    assert test_config.client_id == "test_id"
    assert test_config.client_secret == "test_secret"
    assert test_config.scopes == ["https://graph.microsoft.com/.default"]
    assert test_config.authority == "https://login.microsoftonline.com/common"
    assert test_config.get("tenant_id") is None
