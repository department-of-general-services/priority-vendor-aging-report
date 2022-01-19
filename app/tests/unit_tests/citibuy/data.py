from tests.utils import citibuy_data as mock_data

PO_RESULTS = [
    {
        **mock_data.CONTRACTS["blanket1_DGS"],
        **mock_data.PO_RECORDS["po1"],
        **mock_data.VENDORS["acme"],
        **mock_data.ADDRESSES["acme_mail"],
    },
    {
        **mock_data.CONTRACTS["blanket1_DGS"],
        **mock_data.PO_RECORDS["po1_1"],
        **mock_data.VENDORS["acme"],
        **mock_data.ADDRESSES["acme_mail"],
    },
    {
        **mock_data.CONTRACTS["blanket4"],
        **mock_data.PO_RECORDS["po4"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
    },
    {
        **mock_data.CONTRACTS["blanket4_agy"],
        **mock_data.PO_RECORDS["po4"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
    },
    {
        **mock_data.CONTRACTS["blanket4"],
        **mock_data.PO_RECORDS["po4_1"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
    },
    {
        **mock_data.CONTRACTS["blanket4_agy"],
        **mock_data.PO_RECORDS["po4_1"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
    },
    {
        **mock_data.PO_RECORDS["po5"],
        **mock_data.VENDORS["acme"],
        **mock_data.ADDRESSES["acme_mail"],
        "contract_agency": None,
        "start_date": None,
        "end_date": None,
        "dollar_limit": None,
        "dollar_spent": None,
    },
]
