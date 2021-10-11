import sqlalchemy


class TestPurchaseOrders:
    """Tests the PurchaseOrder class methods"""

    def test_init(self, mock_po):
        """Tests that the PurchaseOrders method inits correctly

        Validates the following test conditions:
        - The class instance inherits self.engine from the CitiBuy class
        - The attribute self.sharepoint is None
        - The attribute self.records is an empty list
        """
        # validation
        assert isinstance(mock_po.engine, sqlalchemy.engine.Engine)
        assert mock_po.sharepoint is None
        assert mock_po.records == []
