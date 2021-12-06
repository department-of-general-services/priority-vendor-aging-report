from pprint import pprint

import pytest
import pandas as pd

from dgs_fiscal.systems.sharepoint.list import (
    ListItem,
    ItemCollection,
    BatchedChanges,
)

ITEM_KEY = {"Title": "Alice"}
QUERY = {"YesNo": ("equals", 1)}


@pytest.fixture(scope="module", name="test_list")
def fixture_list(test_sharepoint):
    """Creates an instance of SiteList for use in integration tests"""
    return test_sharepoint.get_list("API Test")


@pytest.fixture(scope="module", name="test_items")
def fixture_items(test_list):
    """Returns an instance of ItemCollection for testing"""
    return test_list.get_items(query=QUERY)


class TestSiteList:
    """Tests the SiteList methods that make calls to the Graph API"""

    def test_get_items(self, test_items):
        """Tests that the get_items() method executes correctly

        Validates the following conditions:
        - The response returned is an ItemCollection instance
        - The correct set of items are returned
        """
        # validation
        print(test_items.items[0].fields)
        assert len(test_items.items) == 3
        assert isinstance(test_items, ItemCollection)
        assert isinstance(test_items.items[0], ListItem)

    def test_get_item_by_key(self, test_list):
        """Tests that the get_item_by_key() method executes correctly

        Validates the following conditions
        - The response returned is an instance of ListItem
        - The response has the fields attribute set correctly
        """
        # execution
        item = test_list.get_item_by_key(ITEM_KEY)
        # validation
        assert isinstance(item, ListItem)
        assert isinstance(item.fields, dict)

    def test_get_item_by_key_no_match(self, test_list):
        """Tests that the get_item_by_key() method raises a ValueError if
        attempting to get an item with no matching key
        """
        # setup
        fake_key = {"Title": "Fake"}
        with pytest.raises(ValueError):
            test_list.get_item_by_key(fake_key)

    def test_add_item(self, test_list):
        """Tests that the add_items() method executes correctly

        Validates the following conditions:
        - The item has been created in SharePoint
        - The method returns the items as a ListItem
        - All of the values were correctly set
        """
        # setup
        test_data = {
            "Title": "new item",
            "Text": "cat",
            "Favorite Candy": "Butterfinger",
            "YesNo": True,
            "Number": 12,
            # TODO: Figure out how to set Person field
            # "Person": "Daly, William (DGS)",
            "VendorLookupId": "1",
            "Date": "2021-06-22T00:00:00Z",
        }
        # execution
        item = test_list.add_item(test_data)
        # validation
        try:
            assert isinstance(item, ListItem)
            for key, val in test_data.items():
                assert item.get_val(key) == val
        except AssertionError as err:
            raise err
        finally:
            # cleanup
            assert item.item.delete()

    def test_add_item_invalid(self, test_list):
        """Tests that add_item() raises a KeyError when it is provided data
        that has a key that isn't one of the list's existing columns
        """
        # setup
        test_data = {"Fake Col": "new item", "Invoice Number": "new item"}
        # validation
        with pytest.raises(KeyError):
            test_list.add_item(test_data)

    def test_batch_upsert(self, test_list):
        """Tests the the batch_upsert() method

        Validates the following conditions:
        - Each request in the batch response has status 200 or 201
        - An "id" for a list item is included with each request
        """
        # setup
        updates = {"2": {"Favorite Candy": "Butterfinger"}}
        inserts = [{"Title": "Insert 1", "Text": "new val"}]
        changes = BatchedChanges(updates=updates, inserts=inserts)
        # execution
        results = test_list.batch_upsert(changes)
        updates = results.updates
        inserts = results.inserts
        # validation
        for batch in updates + inserts:
            for request in batch:
                assert request["status"] in (200, 201)
                assert "id" in request["body"]


class TestItemCollection:
    """Tests the ItemCollection class methods"""

    def test_filter_items_success(self, test_items):
        """Tests that ItemCollection.filter_items() executes successfully when
        passed a valid filter_key

        Validates the following conditions:
        - The correct number of items are returned
        - The items returned have fields that match the values passed in the
          filter key
        """
        # execution
        items = test_items.filter_items(ITEM_KEY)
        # validation
        assert len(items) == 1
        assert items[0].get_val("Title") == "Alice"
        assert items[0].get_val("Text") == "Foo"

    def test_filter_items_invalid_field(self, test_items):
        """Tests that ItemCollection.filter_items() returns a KeyError when
        passed an invalid filter_key
        """
        # setup
        fake_key = {"Fake Key": "Key"}
        # validation
        with pytest.raises(KeyError):
            test_items.filter_items(fake_key)

    def test_to_dataframe(self, test_items):
        """Tests that ItemCollection.to_dataframe() executes correctly

        Validates the following conditions:
        - The method returns a dataframe
        - The columns have been renamed successfully
        - The dataframe has the correct number of rows
        """
        # execution
        df = test_items.to_dataframe()
        # validation
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert "Favorite Candy" in df.columns


class TestListItem:
    """Tests the ListItem methods that make calls to Graph API"""

    def test_update(self, test_list, test_items):
        """Tests that ListItem.update executes successfully

        Validates the following conditions:
        - ListItem.update() doesn't throw an error
        - The field was successfully updated in SharePoint
        """
        # setup - get item
        item = test_items.filter_items(ITEM_KEY)[0]
        status = item.get_val("Favorite Candy")
        # setup - set update dict
        if status == "MilkyWay":
            data = {"Favorite Candy": "Snickers"}
        else:
            data = {"Favorite Candy": "MilkyWay"}
        # execution
        item.update(data)
        result = test_list.get_item_by_key(ITEM_KEY)
        new_status = result.get_val("Favorite Candy")
        # validation
        assert status != new_status
        assert new_status == data["Favorite Candy"]
