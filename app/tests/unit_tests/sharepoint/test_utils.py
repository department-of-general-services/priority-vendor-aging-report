import pytest

from dgs_fiscal.systems.sharepoint.utils import build_filter_str, col_api_name

COLS = {"Text Col": "TextCol", "Num Col": "NumCol"}


@pytest.mark.parametrize(
    "input_dict, expected",
    [
        ({"Text Col": ("equals", "Text")}, "fields/TextCol eq 'Text'"),
        ({"Text Col": ("not equals", "Text")}, "fields/TextCol ne 'Text'"),
        ({"NumCol": ("greater than", 123)}, "fields/NumCol gt 123"),
        (
            {"Text Col": ("contains", "Text")},
            "contains(fields/TextCol,'Text')",
        ),
        (
            {"TextCol": ("contains", "Text"), "NumCol": ("greater than", 2)},
            "contains(fields/TextCol,'Text') and fields/NumCol gt 2",
        ),
    ],
)
def test_build_filter_str(input_dict, expected):
    """Tests build_filter_str against a number of inputs

    Validates the following conditions:
    - Both display and API names are accepted as filter fields
    - Both relation and function odata types have the correct syntax
    - Both single and multiple filter are built correctly
    """
    # execute
    output = build_filter_str(COLS, input_dict)
    print(output)
    # validate
    assert output == expected


def test_build_filter_str_error():
    """Tests that build_filter_str raises the ColumnNotFoundError when a filter
    dictionary includes a field not found in the list of columns
    """
    # setup
    input_dict = {"Fake Col": ("equals", "Text")}
    # execution
    with pytest.raises(KeyError):
        build_filter_str(COLS, input_dict)


@pytest.mark.parametrize(
    "input_col, expected",
    [
        ("Text Col", "TextCol"),
        ("TextCol", "TextCol"),
        ("TextColLookupId", "TextColLookupId"),
    ],
)
def test_col_api_name(input_col, expected):
    """Tests that col_api_name() executes successfully

    Validates the following conditions:
    - Display name passed to function
    - API name passed to function
    - LookupId passed to function
    """
    # execution
    output = col_api_name(COLS, input_col)
    # validation
    assert output == expected


def test_col_api_name_error():
    """Tests that col_api_name() raises a KeyError if a column name is passed
    that isn't in the list of columns
    """
    # validation
    with pytest.raises(KeyError):
        col_api_name(COLS, "fake_col")
