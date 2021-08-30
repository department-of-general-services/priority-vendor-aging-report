class ColumnNotFound(Exception):
    """Exception raised when attempting to query or update a column that
    doesn't exist within a SharePoint list.
    """

    def __init__(self, missing_col: str, col_list: list) -> None:
        """Inits the ColumnNotInList class

        Parameters
        ----------
        missing_col: str
            The name of the column the user was trying to query or update
        col_list: list
            The list of columns that are found on the SharePoint list
        """
        self.missing_col = missing_col
        self.message = (
            f"{missing_col} not in the list of cols. "
            f"Must be one of the following: {col_list}."
        )
        super().__init__(self.message)
