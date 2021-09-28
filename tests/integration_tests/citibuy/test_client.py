from sqlalchemy import text


class TestCitiBuy:
    """Tests the CitiBuy class"""

    def test_init_success(self, test_citibuy):
        """Tests that the CitiBuy class instantiates correctly

        Validates the following conditions:
        - The output is a list of dicts
        - The output contains the correct columns
        """
        # setup
        query_str = "SELECT TOP 5 PO_NBR, RELEASE_NBR FROM PO_HEADER;"
        # execution
        with test_citibuy.engine.connect() as conn:
            query = text(query_str)
            results = conn.execute(query)
            output = [row._asdict() for row in results.fetchall()]
        # validation
        assert isinstance(output, list)
        assert isinstance(output[0], dict)
        assert list(output[0].keys()) == ["PO_NBR", "RELEASE_NBR"]
