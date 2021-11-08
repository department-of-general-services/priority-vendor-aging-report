import pytest
import sqlalchemy

from dgs_fiscal.systems import CitiBuy


@pytest.fixture(scope="session", name="test_citibuy")
def fixture_citibuy():
    """Creates an instance of the CitiBuy class for integration testing"""
    return CitiBuy()


class TestCitiBuy:
    """Tests the CitiBuy class"""

    def test_init(self, test_citibuy):
        """Tests that the mock CitiBuy db was populated correctly"""
        # validation
        assert isinstance(test_citibuy.engine, sqlalchemy.engine.Engine)
        with pytest.raises(NotImplementedError):
            print(test_citibuy.purchase_orders)
        with pytest.raises(NotImplementedError):
            print(test_citibuy.vendors)
        with pytest.raises(NotImplementedError):
            print(test_citibuy.invoices)
