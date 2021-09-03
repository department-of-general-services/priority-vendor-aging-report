from __future__ import annotations  # prevents NameError for typehints
from typing import Dict

from O365.sharepoint import SharepointList, SharepointListItem


class AgingReportList:
    """Creates an API client for the Priority Vendor Aging SharePoint list

    Facilitates reading/writing to the Priority Vendor Aging SharePoint list
    using the O365 library and the Microsoft Graph API.

    Attributes
    ----------
    site: FiscalSite
        An instance of the FiscalSite class that the Priority Vendor
        Aging list belongs to
    site_list: O365.SharepointList
        An instance of the O365.SharepointList class that manages calls to the
        Lists resource in Graph API
    items: dict[AgingReportItem]
        A list of the items in the PriorityVendorAging SharePoint list
        instantiated as members of the AgingReportItem class
    """

    INVOICE_KEY = ("PONumber", "InvoiceNumber")

    def __init__(
        self,
        site_list: SharepointList,
    ) -> None:
        """Instantiates the AgingReportList class"""
        self.list = site_list
        self.invoices = {}

    def get_invoices(  # pylint: disable = dangerous-default-value
        self,
        fields: tuple = INVOICE_KEY,
        query: Dict[str, tuple] = None,
    ) -> Dict[tuple, AgingReportItem]:
        """Gets items from the Piority Vendor Aging list in SharePoint and
        instantiates them as members of the AgingReportItem class

        Parameters
        ----------
        fields: tuple
            A tuple of the fields that should be included for each item
            returned in the response. Must be members of self.list.columns
        query: dict, optional
            A dictionary that specifies which fields to filter on and what
            filters to apply to them. The keys of the dictionary must be the
            name of a field, and the values should be a tuple of the logical
            operator and the value applied to the logical operator. Default
            is to return all invoices.

        Returns
        -------
        Dict[str, AgingReportItem]
            A list of items from the Priority Vendor Aging SharePoint list
            instantiated as members of the AgingReportItem class
        """
        # query invoice records from SharePoint
        if query:
            pass
        else:
            results = self.list.get_items(expand_fields=list(fields))
        # add them to self.invoices
        for record in results:
            self._init_aging_report_item(record)
        return self.invoices

    def get_invoice_by_key(
        self,
        po_num: str,
        invoice_num: str,
        fields: tuple = INVOICE_KEY,
    ) -> AgingReportItem:
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
        AgingReportItem
            An instance of AgingReportItem for the invoice that matches the
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
            # instantiate result as AgingReportItem
            results = self.list.get_items(query=q, expand_fields=list(fields))
            if not results:
                raise ValueError("No matching invoice found for that key")
            invoice = self._init_aging_report_item(results[0])

        return invoice

    def add_invoices(self, invoice_data: dict) -> AgingReportItem:
        """Inserts a new item into the Priority Vendor Aging list in SharePoint
        and instantiates the result as a member of the AgingReportItem class

        Parameters
        ----------
        invoice_data: dict
            The data that will be used to create a new Priority Vendor Aging
            list item. Keys must be in list of columns and values must match
            the data type for that column

        Returns
        -------
        AgingReportItem
            An instance of AgingReportItem for the list item that was created
        """
        pass

    @property
    def columns(self):
        """Returns the columns in the SharePoint list"""
        return list(self.list.column_name_cw.values())

    def _init_aging_report_item(self, item: SharepointListItem) -> None:
        """Inits invoice as an AgingReportItem and adds it to self.invoices

        Parameters
        ----------
        item: O365.SharepointListItem
            Instance of SharepointListItem used to init AgingReportItem
        """
        # get Invoice and PO Number from fields
        key = tuple(item.fields.get(k) for k in self.INVOICE_KEY)

        # instantiate AgingReportItem and add to self.invoices
        invoice = AgingReportItem(self, item)
        self.invoices[key] = invoice

        return invoice


class AgingReportItem:
    """Creates an API client for an item in the Priority Vendor Aging list

    Facilitates reading and updating items in the Priority Vendor Aging
    SharePoint list using the O365 library and the Microsoft Graph API.

    Attributes
    ----------
    report: AgingReportList
        An instance of the AgingReportList class that the Priority Vendor
        Aging list item belongs to
    item: SharepointListItem
        An instance of the O365.SharepointListItem class that manages calls to
        the ListItems resource in Graph API
    """

    def __init__(
        self,
        report: AgingReportList,
        item: SharepointListItem,
    ) -> None:
        """Instantiates the AgingReportItem class"""
        self.report = report
        self.item = item

    def update(self, **kwargs) -> None:
        """Updates the Priority Vendor Aging list item in SharePoint"""
        pass

    @property
    def fields(self) -> dict:
        """Returns the fields associated with this list item"""
        return self.item.fields
