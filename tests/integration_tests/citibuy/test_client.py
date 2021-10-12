import pytest
import sqlalchemy


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
