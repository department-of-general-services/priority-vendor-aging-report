import pytest
from sqlalchemy.exc import ProgrammingError


class TestCitiBuy:
    """Tests the CitiBuy class"""

    def test_query_success(self, test_citibuy):
        """Tests the CitiBuy.query() method against valid SQL

        Validates the following conditions:
        - The CitiBuy class instantiates without error
        - The query() method executes without error
        - The output returned is a list of dicts
        - The output returned contains the correct columns
        """
        # setup
        query_str = "SELECT TOP 5 PO_NBR, RELEASE_NBR FROM PO_HEADER;"
        # execution
        output = test_citibuy.query(query_str)
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert list(output[0].keys()) == ["PO_NBR", "RELEASE_NBR"]

    def test_query_invalid_sql(self, test_citibuy):
        """Tests that CitiBuy.query() raises a ProgrammingError when passed
        the string of an invalid SQL query
        """
        # setup
        query_str = "SELECT TOP 5 cols FROM fake_table;"
        # execution
        with pytest.raises(ProgrammingError):
            test_citibuy.query(query_str)
