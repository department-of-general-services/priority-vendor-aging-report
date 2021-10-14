from __future__ import annotations  # prevents NameError for typehints
from typing import Dict, Type, List, Iterable

from O365.sharepoint import SharepointList, SharepointListItem

from aging_report.sharepoint.utils import build_filter_str, get_col_api_name


class ListBase:
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
        A list of the items in the PriorityVendorAging SharePoint list
        instantiated as members of the InvoiceItem class
    """

    INVOICE_KEY = ("PONumber", "InvoiceNumber")

    def __init__(self, site_list: SharepointList) -> None:
        """Instantiates the InvoiceList class"""
        self.list = site_list

    def get_items(  # pylint: disable = dangerous-default-value
        self,
        fields: Iterable,
        query: Dict[str, tuple] = None,
    ) -> List[SharepointListItem]:
        """Gets items from the SharePoint List and returns a list of
        SharepointListItem instances

        Parameters
        ----------
        fields: tuple
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
        if query:
            q = build_filter_str(self.columns, query)
        return self.list.get_items(query=q, expand_fields=list(fields))

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

    @property
    def columns(self) -> dict:
        """Returns the columns in the SharePoint list"""
        return self.list.column_name_cw


class ListItemBase:
    """Creates an API client for making calls to the SharePoint list item

    Attributes
    ----------
    parent: Type[ListBase]
        An instance of the ListBase sub-class that this item belongs to
    item: o365.SharepointListItem
        An instance of the O365.SharepointListItem class that manages calls to
        the ListItems resource in Graph API
    """

    def __init__(
        self,
        parent: Type[ListBase],
        item: SharepointListItem,
    ) -> None:
        """Instantiates the ListItemBase class"""
        self.parent = parent
        self.item = item

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

    @property
    def fields(self) -> dict:
        """Returns the fields associated with this list item"""
        return self.item.fields
