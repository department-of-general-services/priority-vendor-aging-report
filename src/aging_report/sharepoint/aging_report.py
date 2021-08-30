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

    INVOICE_FIELDS = ("InvoiceNumber", "PONumber")
    FILTER_OPERATORS = (
        "equals",
        "not equals",
        "contains",
        "starts with",
    )

    def __init__(
        self,
        site_list: SharepointList,
    ) -> None:
        """Instantiates the AgingReportList class"""
        self.list = site_list
        self.invoices = {}

    def get_invoices(  # pylint: disable = dangerous-default-value
        self,
        fields: tuple = INVOICE_FIELDS,
        query: Dict[str, tuple] = {"Status": ("not equals", "Paid")},
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
            is to exclude all paid invoices.

        Returns
        -------
        Dict[str, AgingReportItem]
            A list of items from the Priority Vendor Aging SharePoint list
            instantiated as members of the AgingReportItem class
        """
        if query:
            pass

        # query invoice records from SharePoint
        results = self.list.get_items(expand_fields=list(fields))

        # instantiate each record as an AgingReportItem
        for record in results:
            invoice = AgingReportItem(self, record)

            # add it to self.invoices keyed by (PO number, invoice number)
            po_num = record.fields.get("PONumber")
            invoice_num = record.fields.get("InvoiceNumber")
            invoice_key = (po_num, invoice_num)
            print(invoice_key)
            self.invoices[invoice_key] = invoice

        return self.invoices

    def get_invoice_by_key(
        self, po_num: str, invoice_num: str
    ) -> AgingReportItem:
        """Return a single invoice keyed by Invoice Number and PO Number"""

        # first, check the list of existing invoices
        invoice_key = (po_num, invoice_num)
        invoice = self.invoices.get(invoice_key)

        # if none found, query the invoice from SharePoint
        if not invoice:
            # filter items on invoice number and po number
            q = self.list.new_query()
            q.on_attribute("InvoiceNumber").equals(invoice_num)
            q.chain("and").on_attribute("PONumber").equals(po_num)
            # instantiate result as AgingReportItem
            results = self.list.get_items(query=q)
            invoice = AgingReportItem(self, results[0])

        return invoice

    def add_invoices(self, **kwargs) -> None:
        """Inserts a new item into the Priority Vendor Aging list in SharePoint
        and instantiates the result as a member of the AgingReportItem class
        """
        pass


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
        self.id = item.object_id

    def update(self, **kwargs) -> None:
        """Updates the Priority Vendor Aging list item in SharePoint"""
        pass
