from dgs_fiscal.systems.sharepoint import BatchedChanges


class TestBatchedChanges:
    """Tests the BatchedChanges dataclass"""

    UPDATES = {"test_id": {"test_col": "test_val"}}
    INSERTS = [{"test_col": "test_val"}]

    def test_init_empty(self):
        """Tests that the BatchedChanges dataclass inits correctly without
        any data passed to it

        Validates the following conditions:
        - The dataclass inits without error
        - New items can be added to BatchedChanges.updates
        - New items can be added to BatchedChanges.inserts
        """
        # execution - empty
        batch = BatchedChanges()
        # validation - empty
        assert batch.updates == {}
        assert batch.inserts == []
        # execution - adding items
        for key, val in self.UPDATES.items():
            batch.updates[key] = val
        batch.inserts.extend(self.INSERTS)
        # validation - adding items
        assert batch.updates == self.UPDATES
        assert batch.inserts == self.INSERTS

    def test_init_with_data(self):
        """Tests that the BatchedChanges dataclass inits correctly when data
        is passed to it

        Validates the following conditions:
        - The dataclass inits without error
        - New items can be added to BatchedChanges.updates
        - New items can be added to BatchedChanges.inserts
        """
        # execution - empty
        batch = BatchedChanges(updates=self.UPDATES, inserts=self.INSERTS)
        # validation - adding items
        assert batch.updates == self.UPDATES
        assert batch.inserts == self.INSERTS
