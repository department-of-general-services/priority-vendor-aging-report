class AgingReportList:
    """Uses the Graph API to read from and write to the Priority Vendor Aging
    SharePoint list. This class inherits from the SitesList base class.
    """

    def __init__(self) -> None:
        """Instantiates the AgingReportList class"""

        self.items = None
        self.client = None

    def get_invoices(self) -> None:
        """Gets items from the Piority Vendor Aging list in SharePoint and
        instantiates them as members of the AgingReportItem class
        """
        pass

    def add_invoices(self, **kwargs) -> None:
        """Inserts a new item into the Priority Vendor Aging list in SharePoint
        and instantiates the result as a member of the AgingReportItem class
        """
        pass


class AgingReportItem:
    """Uses the Graph API to read, update, and delete items in the Priority
    Vendor Aging list in SharePoint. This class inherits from the SitesListItem
    base class.
    """

    def __init__(self, **kwargs) -> None:
        """Instantiates the AgingReportItem class"""
        pass

    def update(self, **kwargs) -> None:
        """Updates the Priority Vendor Aging list item in SharePoint"""
        pass
