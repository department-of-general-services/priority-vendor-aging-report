from datetime import datetime

from tests.utils import citibuy_data as mock_data

PO_RESULTS = [
    {
        **mock_data.CONTRACTS["blanket1_DGS"],
        **mock_data.PO_RECORDS["po1"],
        **mock_data.VENDORS["acme"],
        **mock_data.ADDRESSES["acme_mail"],
        "unit": mock_data.LOCATIONS["building"]["desc"],
    },
    {
        **mock_data.CONTRACTS["blanket1_DGS"],
        **mock_data.PO_RECORDS["po1_1"],
        **mock_data.VENDORS["acme"],
        **mock_data.ADDRESSES["acme_mail"],
        "unit": mock_data.LOCATIONS["fleet"]["desc"],
    },
    {
        **mock_data.CONTRACTS["blanket4"],
        **mock_data.PO_RECORDS["po4"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
        "unit": mock_data.LOCATIONS["dpw"]["desc"],
    },
    {
        **mock_data.CONTRACTS["blanket4_agy"],
        **mock_data.PO_RECORDS["po4"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
        "unit": mock_data.LOCATIONS["dpw"]["desc"],
    },
    {
        **mock_data.CONTRACTS["blanket4"],
        **mock_data.PO_RECORDS["po4_1"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
        "unit": mock_data.LOCATIONS["energy"]["desc"],
    },
    {
        **mock_data.CONTRACTS["blanket4_agy"],
        **mock_data.PO_RECORDS["po4_1"],
        **mock_data.VENDORS["disney"],
        **mock_data.ADDRESSES["disney_mail"],
        "unit": mock_data.LOCATIONS["energy"]["desc"],
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
        "unit": mock_data.LOCATIONS["contract"]["desc"],
    },
]

INVOICE_RESULTS = [
    {
        # P111:1
        **mock_data.INVOICES["inv2"],
        "vendor_name": "Acme",
        "po_status": "3PPR",
        "po_date": None,
        "po_cost": 75.00,
        "contract_end_date": datetime(2050, 7, 1),
        "contract_dollar_limit": 750.00,
        "contract_amount_spent": 50.00,
    },
    {
        # P111:1
        **mock_data.INVOICES["inv3"],
        "vendor_name": "Acme",
        "po_status": "3PPR",
        "po_date": None,
        "po_cost": 75.00,
        "contract_end_date": datetime(2050, 7, 1),
        "contract_dollar_limit": 750.00,
        "contract_amount_spent": 50.00,
    },
    {
        # P222
        **mock_data.INVOICES["inv5"],
        "vendor_name": "Disney",
        "po_status": "3PCO",
        "po_date": None,
        "po_cost": 15.50,
        "contract_end_date": None,
        "contract_dollar_limit": None,
        "contract_amount_spent": None,
    },
    {
        # P222
        **mock_data.INVOICES["inv6"],
        "vendor_name": "Disney",
        "po_status": "3PCO",
        "po_date": None,
        "po_cost": 15.50,
        "contract_end_date": None,
        "contract_dollar_limit": None,
        "contract_amount_spent": None,
    },
    {
        # P444:1
        **mock_data.INVOICES["inv8"],
        "vendor_name": "Disney",
        "po_status": "3PPR",
        "po_date": None,
        "po_cost": 10.00,
        "contract_end_date": datetime(2050, 7, 1),
        "contract_dollar_limit": 10000.00,
        "contract_amount_spent": 250.00,
    },
]


RECEIPT_RESULTS = [
    {
        **mock_data.RECEIPTS["receipt1"],
        "approval_nbr": 1,
        "approver": "JOHNSMITH",
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "unit": mock_data.LOCATIONS["building"]["desc"],
        "approval_date": None,
    },
    {
        **mock_data.RECEIPTS["receipt2"],
        "approval_nbr": 1,
        "approver": "JANEDOE",
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "unit": mock_data.LOCATIONS["fleet"]["desc"],
        "approval_date": None,
    },
    {
        **mock_data.RECEIPTS["receipt2"],
        "approval_nbr": 1,
        "approver": "JOHNSMITH",
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "unit": mock_data.LOCATIONS["fleet"]["desc"],
        "approval_date": None,
    },
    {
        **mock_data.RECEIPTS["receipt3"],
        "approval_nbr": 1,
        "approver": "JOHNSMITH",
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "unit": mock_data.LOCATIONS["building"]["desc"],
        "approval_date": datetime(2025, 9, 1),
    },
]
