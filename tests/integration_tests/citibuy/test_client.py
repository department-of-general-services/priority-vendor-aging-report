from aging_report.citibuy import CitiBuy


class TestCitiBuy:
    """Tests the CitiBuy class"""

    def test_init_success(self):
        """Tests that the CitiBuy class instantiates correctly"""
        # setup
        CitiBuy()
        # validation
        assert 1
