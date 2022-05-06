from dgs_fiscal.config import settings


def test_config_prod():
    """Tests that all of the correct secrets are configured in the settings"""
    # setup
    secrets = [
        "client_id",
        "client_secret",
        "tenant_id",
        "host_name",
        "site_name",
        "site_id",
        "drive_id",
        "archive_id",
        "core_url",
        "core_username",
        "core_password",
        "chrome_driver_path",
        "citibuy_server",
        "citibuy_db",
        "citibuy_username",
        "citibuy_password",
    ]
    # validation
    for secret in secrets:
        value = settings.get(secret)
        assert value is not None, f"{secret} wasn't set"
        assert "test" not in value, f"{secret} still has default value"
