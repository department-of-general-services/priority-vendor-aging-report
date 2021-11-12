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
        # setup
        query = "SELECT TOP 5 PO_NBR, RELEASE_NBR FROM PO_HEADER"
        # execution
        results = test_citibuy.execute_stmt(query)
        print(results.records)
        # validation
        assert isinstance(test_citibuy.engine, sqlalchemy.engine.Engine)
        assert isinstance(results.records, list)
        assert len(results.records) == 5
