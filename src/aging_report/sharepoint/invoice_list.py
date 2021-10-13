from __future__ import annotations  # prevents NameError for typehints
from typing import Dict

from O365.sharepoint import SharepointList, SharepointListItem

from aging_report.sharepoint.utils import build_filter_str, get_col_api_name
from aging_report.sharepoint import ListBase, ListItemBase


class InvoiceList(ListBase):
    """Creates an API client for the Priority Vendor Aging SharePoint list

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
        self.invoices = {}

    def get_invoices(  # pylint: disable = dangerous-default-value
        self,
        fields: tuple = INVOICE_KEY,
        query: Dict[str, tuple] = None,
    ) -> Dict[tuple, InvoiceItem]:
        """Gets items from the Piority Vendor Aging list in SharePoint and
        instantiates them as members of the InvoiceItem class

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
        Dict[str, InvoiceItem]
            A list of items from the Priority Vendor Aging SharePoint list
            instantiated as members of the InvoiceItem class
        """
        # query the results
        results = super().get_items(fields, query)
        # add them to self.invoices
        for record in results:
            self._init_invoice_item(record)
        return self.invoices

    def get_invoice_by_key(
        self,
        po_num: str,
        invoice_num: str,
        fields: tuple = INVOICE_KEY,
    ) -> InvoiceItem:
        """Return a single invoice keyed by Invoice Number and PO Number

        Parameters
        ----------
        po_num: str,
            The PO Number associated with the invoice being queried
        invoice_num: str,
            The Invoice Number associated with the invoice being queried
        fields: tuple, optional
            The list item fields that should be returned by the query. Default
            is to only return Invoice and PO Number.

        Returns
        -------
        InvoiceItem
            An instance of InvoiceItem for the invoice that matches the
            Invoice and PO Number
        """
        # first, check the list of existing invoices
        invoice_key = (po_num, invoice_num)
        invoice = self.invoices.get(invoice_key)

        # if none found, query the invoice from SharePoint
        if not invoice:
            q = (
                f"fields/PONumber eq '{po_num}' and "
                f"fields/InvoiceNumber eq '{invoice_num}'"
            )
            # instantiate result as InvoiceItem
            results = self.list.get_items(query=q, expand_fields=list(fields))
            if not results:
                raise ValueError("No matching invoice found for that key")
            invoice = self._init_invoice_item(results[0])

        return invoice

    def add_invoices(self, invoice_data: dict) -> InvoiceItem:
        """Inserts a new item into the Priority Vendor Aging list in SharePoint
        and instantiates the result as a member of the InvoiceItem class

        Parameters
        ----------
        invoice_data: dict
            The data that will be used to create a new Priority Vendor Aging
            list item. Keys must be in list of columns and values must match
            the data type for that column

        Returns
        -------
        InvoiceItem
            An instance of InvoiceItem for the list item that was created
        """
        pass

    def _init_invoice_item(self, item: SharepointListItem) -> None:
        """Inits invoice as an InvoiceItem and adds it to self.invoices

        Parameters
        ----------
        item: O365.SharepointListItem
            Instance of SharepointListItem used to init InvoiceItem
        """
        # get Invoice and PO Number from fields
        key = tuple(item.fields.get(k) for k in self.INVOICE_KEY)

        # instantiate InvoiceItem and add to self.invoices
        invoice = InvoiceItem(self, item)
        self.invoices[key] = invoice

        return invoice


class InvoiceItem(ListItemBase):
    """Creates an API client for an item in the Priority Vendor Aging list

    Facilitates reading and updating items in the Priority Vendor Aging
    SharePoint list using the O365 library and the Microsoft Graph API.

    Attributes
    ----------
    parent: InvoiceList
        An instance of the InvoiceList class that the Priority Vendor
        Aging list item belongs to
    item: SharepointListItem
        An instance of the O365.SharepointListItem class that manages calls to
        the ListItems resource in Graph API
    """

    def __init__(
        self,
        parent: InvoiceList,
        item: SharepointListItem,
    ) -> None:
        """Instantiates the InvoiceItem class"""
        super().__init__(parent, item)

    def update(self, data: dict) -> None:
        """Updates the Priority Vendor Aging list item in SharePoint

        Parameters
        ----------
        data: dict
            A dictionary of {"field name": new_value} used to update the fields
        """
        super().update(data)
