from dgs_fiscal.systems.core_integrator.scraper import CoreIntegrator


class TestCoreIntegrator:
    """Manages unit tests for CoreIntegrator class"""

    def test_init(self):
        """Tests that CoreIntegrator instantiates correctly"""
        # execution
        CoreIntegrator()
        # validation
        assert 1
