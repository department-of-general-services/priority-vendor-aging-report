from __future__ import annotations  # prevents NameError for typehints
from typing import Dict, List, Iterable, Any, Optional
from dataclasses import dataclass, field

import pandas as pd
from O365.sharepoint import SharepointList, SharepointListItem

from dgs_fiscal.systems.sharepoint.utils import build_filter_str, col_api_name


@dataclass
class BatchedChanges:
    """Data class for grouping bulk changes to a SharePoint list

    Attributes
    ----------
    updates: Dict[dict], optional
        A dictionary of the updates with the following format:
        {"list item id": {"field name": "new value"}}
    inserts: List[dict], optional
        A list of the new items to insert into the list, with the following
        format: [{"field name": "value", "field name": "value"}]
    """

    updates: Optional[Dict[dict]] = field(default_factory=dict)
    inserts: Optional[List[dict]] = field(default_factory=list)


class SiteList:
    """Creates an API client for making calls to the SharePoint list resource

    Attributes
    ----------
    site: FiscalSite
        An instance of the FiscalSite class that the Priority Vendor
        Aging list belongs to
    site_list: O365.SharepointList
        An instance of the O365.SharepointList class that manages calls to the
        Lists resource in Graph API
    items: dict[InvoiceItem]
        A dictionary of the items in SharePoint list instantiated as members
        of the InvoiceItem class and keyed by the columns in self.key
    """

    def __init__(self, site_list: SharepointList, key: list = None) -> None:
        """Instantiates the SiteList class"""
        self.list = site_list
        self.key = key

    @property
    def columns(self) -> dict:
        """Returns the columns in the SharePoint list"""
        return self.list.column_name_cw

    def get_items(  # pylint: disable = dangerous-default-value
        self,
        fields: Iterable = None,
        query: Dict[str, tuple] = None,
    ) -> List[SharepointListItem]:
        """Gets items from the SharePoint List and returns a list of
        SharepointListItem instances

        Parameters
        ----------
        fields: tuple, optional
            A tuple of the fields that should be included for each item
            returned in the response. Must be members of self.list.columns
        query: dict, optional
            A dictionary of {"field name": ("operator": "condition")} used to
            filter the results. Default is to return all invoices.

        Returns
        -------
        List[SharepointListItem]
            A list of items from the SharePoint list instantiated as members
            of the o365.SharepointListItem class
        """
        # query invoice records from SharePoint
        fields = fields or self.columns.keys()
        if query:
            query = build_filter_str(self.columns, query)
        results = self.list.get_items(query=query, expand_fields=list(fields))
        if not results:
            raise ValueError("No matching item found for that query")
        items = [ListItem(self, item) for item in results]
        return ItemCollection(self, items, fields)

    def get_item_by_key(self, key: dict, fields: Iterable = None) -> ListItem:
        """Returns a single list item that matches the values passed to the key

        Parameters
        ----------
        key: dict
            A dictionary of the column(s) and value(s) used to lookup the item.
            Dictionary must match the format: {"key_col": "lookup value"}

        Returns
        -------
        ListItem
            A ListItem instance for the item that matches the lookup key
        """
        # get items using key as a query
        fields = fields or self.columns.keys()
        query = {k: ("equals", v) for k, v in key.items()}
        results = self.get_items(fields, query)
        return results.items[0]

    def add_item(self, data: dict) -> ListItem:
        """Inserts a new item into the SharePoint list and returns an instance
        of o365.SharepointListItem

        Parameters
        ----------
        data: dict
            The data that will be used to create a new Priority Vendor Aging
            list item. Keys must be in list of columns and values must match
            the data type for that column

        Returns
        -------
        ListItem
            A ListItem instance for the item that was created in SharePoint
        """
        data = self._format_request_data(data)
        item = self.list.create_list_item(data)
        return ListItem(self, item)

    def batch_upsert(self, changes: BatchedChanges) -> dict:
        """Submits batch requests to update or insert list items

        Parameters
        ----------
        changes: BatchedChanges
            Instance of BatchedChanges dataclass which contains the items
            to update or insert into this SharePoint list

        Returns
        -------
        dict
            A dictionary of the JSON response from a batch request
        """
        batch_url = "https://graph.microsoft.com/v1.0/$batch"
        base_url = f"/{self.list.main_resource}"
        requests = []
        counter = 0

        if changes.updates:
            for item_id, data in changes.updates.items():
                counter += 1
                url = base_url + f"/items/{item_id}/fields"
                request = self._build_request(counter, data, url, "PATCH")
                requests.append(request)

        if changes.inserts:
            for data in changes.inserts:
                counter += 1
                url = base_url + "/items"
                request = self._build_request(counter, data, url, "POST")
                requests.append(request)

        response = self.list.con.post(batch_url, {"requests": requests})
        return response.json()

    def _build_request(
        self,
        counter: int,
        data: dict,
        url: str,
        method: str,
    ) -> dict:
        """Builds an entry to add to a batch request entry"""
        request_data = self._format_request_data(data)
        if method == "POST":
            request_data = {"fields": request_data}
        request = {
            "id": str(counter),
            "url": url,
            "method": method,
            "body": request_data,
            "headers": {"Content-Type": "application/json"},
        }
        return request

    def _format_request_data(self, data) -> dict:
        """Get the API col name for each column in the request data"""
        return {col_api_name(self.columns, k): v for k, v in data.items()}


class ItemCollection:
    """A collection of ListItem instances that support aggregate operations

    Attributes:
    list: SiteList
        The instance of SiteList representing the SharePoint list
        that the ItemCollection was returned from
    items: List[ListItem]
        A list of instances of the ListItem class that represent items in a
        SharePoint list returned by SiteList.get_items()
    columns: list
        A list of the fields that were returned for each item in the collection
    """

    def __init__(
        self,
        site_list: SiteList,
        items: List[ListItem],
        cols: list,
    ) -> None:
        """Instantiates the ItemCollection class"""
        self.items = items
        self.list = site_list
        self.columns = cols

    def filter_items(self, filter_key: dict) -> List[ListItem]:
        """Searches through self._items to find items based on the value
        of their field(s)

        Parameters
        ----------
        filter_key: dict
            Dictionary of fields and values used to search through self._items

        Returns
        -------
            A list of ListItem instances or an empty list if no matching
            items were found based on the search key
        """
        matches = []

        # check that the filter key is a valid columns
        for col in filter_key.keys():
            if col not in self.columns:
                raise KeyError(
                    f"{col} is isn't included in the list of fields "
                    "returned from SharePoint by SiteList.get_items()"
                )

        # iterate through items
        for item in self.items:
            matched = True
            # check the fields against the search key
            for key, val in filter_key.items():
                # if any don't match, move to the next item
                if item.get_val(key) != val:
                    matched = False
                    break
            # if all keys match append it to the list
            if matched:
                matches.append(item)
        return matches

    def to_dataframe(self, include_id=False) -> pd.DataFrame:
        """Exports the list of items and their fields as a dataframe"""
        # convert items to dataframe
        if include_id:
            items = [{"id": item.id, **item.fields} for item in self.items]
        else:
            items = [item.fields for item in self.items]
        df = pd.DataFrame(items)
        # rename the columns
        cols = self.list.columns
        rename_cols = {col_api_name(cols, c): c for c in self.columns}
        return df.rename(columns=rename_cols)


class ListItem:
    """Creates an API client for making calls to the SharePoint list item

    Attributes
    ----------
    parent: Type[SiteList]
        An instance of the SiteList sub-class that this item belongs to
    item: o365.SharepointListItem
        An instance of the O365.SharepointListItem class that manages calls to
        the ListItems resource in Graph API
    """

    def __init__(
        self,
        parent: SiteList,
        item: SharepointListItem,
    ) -> None:
        """Instantiates the ListItem class"""
        self.parent = parent
        self.item = item

    @property
    def fields(self) -> dict:
        """Returns the fields associated with this list item"""
        return self.item.fields

    @property
    def id(self) -> dict:
        """Returns the SharePoint id for this list item"""
        return self.item.object_id

    def update(self, data: dict) -> None:
        """Updates the list item in SharePoint

        Parameters
        ----------
        data: dict
            A dictionary of {"field name": new_value} used to update the fields
        """
        # gets api name for each field in update data
        cols = self.parent.columns
        data = {col_api_name(cols, col): val for col, val in data.items()}
        # adds field to self.fields to avoid update error
        for col in data:
            if col not in self.fields:
                self.fields[col] = None

        # update and save field
        self.item.update_fields(data)
        self.item.save_updates()

    def get_val(self, column) -> Any:
        """Returns the value of an item's field"""
        col = col_api_name(self.parent.columns, column)
        return self.fields.get(col)
