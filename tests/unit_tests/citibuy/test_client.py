import pytest
import sqlalchemy
from sqlalchemy.exc import OperationalError


class TestCitiBuy:
    """Unit tests for the CitiBuy class"""

    def test_init(self, mock_db, mock_citibuy):
        """Tests that the mock CitiBuy db was populated correctly"""
        # validation
        assert mock_db.exists()
        assert isinstance(mock_citibuy.engine, sqlalchemy.engine.Engine)

    def test_query_success(self, mock_citibuy):
        """Tests the CitiBuy.query() method against valid SQL

        Validates the following conditions:
        - The CitiBuy class instantiates without error
        - The query() method executes without error
        - The output returned is a list of dicts
        - The output returned contains the correct columns
        """
        # setup
        query_str = "SELECT PO_NBR, RELEASE_NBR FROM PO_HEADER;"
        # execution
        output = mock_citibuy.query(query_str)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert list(output[0].keys()) == ["PO_NBR", "RELEASE_NBR"]

    def test_query_invalid_sql(self, mock_citibuy):
        """Tests that CitiBuy.query() raises a ProgrammingError when passed
        the string of an invalid SQL query
        """
        # setup
        query_str = "SELECT cols FROM fake_table;"
        # execution
        with pytest.raises(OperationalError):
            mock_citibuy.query(query_str)
