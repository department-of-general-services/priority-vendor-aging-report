from __future__ import annotations  # prevents NameError for typehints
from typing import Dict, List, Iterable, Any

from O365.sharepoint import SharepointList, SharepointListItem

from aging_report.sharepoint.utils import build_filter_str, get_col_api_name


class BaseList:
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
        """Instantiates the BaseList class"""
        self.list = site_list
        self.key = key
        self._items = {}

    @property
    def columns(self) -> dict:
        """Returns the columns in the SharePoint list"""
        return self.list.column_name_cw

    @property
    def items(self) -> List[BaseItem]:
        """Returns the list of items queried from SharePoint"""
        if not self._items:
            raise NotImplementedError("No list items have been quried yet")
        return list(self._items.values())

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
        fields = fields or self.columns.values()
        if query:
            q = build_filter_str(self.columns, query)
        results = self.list.get_items(query=q, expand_fields=list(fields))
        if not results:
            return []
        items = [self._init_item(item) for item in results]
        return items

    def get_item_by_key(self, key: dict, fields: Iterable = None) -> BaseItem:
        """Returns a single list item that matches the values passed to the key

        Parameters
        ----------
        key: dict
            A dictionary of the column(s) and value(s) used to lookup the item.
            Dictionary must match the format: {"key_col": "lookup value"}

        Returns
        -------
        BaseItem
            A BaseItem instance for the item that matches the lookup key
        """
        # search through existing item list
        results = self.find_items_by_field(key)

        # if no match is found, query it from SharePoint
        if not results:
            fields = fields or self.columns.keys()
            query = {k: ("equals", v) for k, v in key.items()}
            results = self.get_items(fields, query)

        # if a match still isn't found, raise an error
        if not results:
            raise ValueError("No matching item found for that key")
        return results[0]

    def add_items(self, data: dict) -> List[SharepointListItem]:
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
        o365.SharePointListItem
            A o365.SharepointListItem instance for the item that was created
        """
        pass

    def _init_item(self, item: SharepointListItem) -> None:
        """Inits list item as an BaseListItem and adds it to self._items

        Parameters
        ----------
        item: O365.SharepointListItem
            Instance of SharepointListItem used to init BaseItem
        fields: Iterable
            The set of fields that should be added to item
        """
        list_item = BaseItem(self, item)
        self._items[item.object_id] = list_item
        return list_item

    def find_items_by_field(self, search_key: dict) -> List[BaseItem]:
        """Searches through self._items to find items based on the value
        of their field(s)

        Parameters
        ----------
        search_key: dict
            Dictionary of fields and values used to search through self._items

        Returns
        -------
            A list of BaseItem instances or an empty list if no matching
            items were found based on the search key
        """
        matches = []
        if not self._items:
            return matches
        # iterate through items
        for item in self._items.values():
            matched = True
            # check the fields against the search key
            for key, val in search_key.items():
                # if any don't match, move to the next item
                if item.get(key) != val:
                    matched = False
                    break
            # if all keys match append it to the list
            if matched:
                matches.append(item)
        return matches


class BaseItem:
    """Creates an API client for making calls to the SharePoint list item

    Attributes
    ----------
    parent: Type[BaseList]
        An instance of the BaseList sub-class that this item belongs to
    item: o365.SharepointListItem
        An instance of the O365.SharepointListItem class that manages calls to
        the ListItems resource in Graph API
    """

    def __init__(
        self,
        parent: BaseList,
        item: SharepointListItem,
    ) -> None:
        """Instantiates the BaseItem class"""
        self.parent = parent
        self.item = item

    @property
    def fields(self) -> dict:
        """Returns the fields associated with this list item"""
        return self.item.fields

    def update(self, data: dict) -> None:
        """Updates the list item in SharePoint

        Parameters
        ----------
        data: dict
            A dictionary of {"field name": new_value} used to update the fields
        """
        # gets api name for each field in update data
        cols = self.parent.columns
        data = {get_col_api_name(cols, col): val for col, val in data.items()}
        # adds field to self.fields to avoid update error
        for field in data:
            if field not in self.fields:
                self.fields[field] = None

        # update and save field
        self.item.update_fields(data)
        self.item.save_updates()

    def get(self, field) -> Any:
        """Returns the value of an item's field"""
        col = get_col_api_name(self.parent.columns, field)
        return self.fields.get(col)
