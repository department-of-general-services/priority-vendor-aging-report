from __future__ import annotations  # prevents NameError for typehints

from dynaconf import Dynaconf
from O365 import Account

from aging_report.errors import ColumnNotFoundError


QUERY_MAPPING = {
    "equals": ("relation", "eq"),
    "not equals": ("relation", "ne"),
    "greater than": ("relation", "gt"),
    "less than": ("relation", "lt"),
    "greater or equal": ("relation", "ge"),
    "less or equal": ("relation", "le"),
    "contains": ("function", "contains"),
    "starts with": ("function", "startsWith"),
    "ends with": ("function", "endsWith"),
}


def authenticate_account(config: Dynaconf) -> Account:
    """Creates and authenticates an O365.Account instance

    Parameters
    ----------
    config: Dynaconf
        The config settings that will be used to authenticate the account with
        Microsoft Graph API

    Returns
    -------
    Account
        An instance of the Account class from O365 that has been authenticated
    """
    credentials = (config.client_id, config.client_secret)
    account = Account(
        credentials,
        auth_flow_type="credentials",
        tenant_id=config.tenant_id,
    )
    if not account.is_authenticated:
        account.authenticate()
    return account


def build_filter_str(columns: dict, query_dict: dict) -> str:
    """Converts a query dictionary to a string that conforms to the OData query
    format and can be passed to the query parameter in O365 get methods

    Parameters
    ----------
    cols: dict
        A dictionary of the columns to filter on, with the display name of each
        column as the key and the API name as the value
    query_dict: dict
        A dictionary that specifies which fields to filter on and what
        filters to apply to them. The keys of the dictionary must be the
        name of a field, and the values should be a tuple of the logical
        operator and the value applied to the logical operator.

    Returns
    -------
    str
        A string of the OData compliant query that will be passed to the O365
        library and included in the resource request URL

    Notes
    -----
    For more information about OData query syntax view the following links:
    - https://www.odata.org/getting-started/basic-tutorial/#queryData
    - https://docs.microsoft.com/en-us/graph/query-parameters#filter-parameter
    """
    prefix = "fields/"

    # iteratively create filters
    filters = []
    for col, condition in query_dict.items():
        # check that filter field is in list of columns
        if col in columns:
            field = prefix + columns[col]
        elif col in columns.values():
            field = prefix + col
        else:
            raise ColumnNotFoundError(col, columns)

        # build filter using odata syntax mapping
        operator, value = condition
        if isinstance(value, str):
            value = f"'{value}'"
        odata_type, syntax = QUERY_MAPPING[operator]
        if odata_type == "relation":
            filters.append(f"{field} {syntax} {value}")
        elif odata_type == "function":
            filters.append(f"{syntax}({field},{value})")

    # create string from filters
    if len(filters) > 1:
        query_str = " and ".join(filters)
    else:
        query_str = filters[0]

    return query_str
