import pytest

from dgs_fiscal.etl import PromptPayment
from dgs_fiscal.systems import CoreIntegrator, SharePoint


@pytest.fixture(scope="session", name="test_prompt")
def fixture_prompt_payment(test_archive_dir):
    """Creates a fixture of the PromptPayment class for testing"""
    return PromptPayment(local_archive=test_archive_dir)


class TestPromptPayment:
    """Tests the PromptPayment etl class"""

    def test_init(self, test_prompt, test_archive_dir):
        """Tests that the PromptPayment inits correctly"""
        # validation
        assert test_prompt.archive.archive_dir == test_archive_dir
        assert isinstance(test_prompt.core_integrator, CoreIntegrator)
        assert isinstance(test_prompt.sharepoint, SharePoint)
