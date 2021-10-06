def test_db(mock_db):
    """Tests that the mock CitiBuy db was populated correctly"""
    assert mock_db.exists()
