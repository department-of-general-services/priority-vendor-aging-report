from datetime import datetime

VENDORS = {
    "acme": {
        "vendor_id": "111",
        "name": "Acme",
        "emg_contact": "Jane Doe",
        "emg_email": "jane.doe@acme.com",
        "emg_phone": "(111) 111-1111",
    },
    "disney": {
        "vendor_id": "222",
        "name": "Disney",
        "emg_contact": "Anthony Williams",
        "emg_email": "anthony.williams@disney.com",
        "emg_phone": "(222) 222-2222",
    },
}

VEN_ADDRESS = {
    "acme_mail": {
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "address_id": "111",
        "address_type": "M",
        "default": "Y",
    },
    "acme_extra": {
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "address_id": "222",
        "address_type": "R",
        "default": "Y",
    },
    "disney": {
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "address_id": "333",
        "address_type": "M",
        "default": "Y",
    },
}

ADDRESSES = {
    "acme_mail": {
        "address_id": "111",
        "contact": "Jane Doe",
        "email": "jane.doe@acme.com",
        "phone": "(111) 111-1111",
    },
    "acme_extra": {
        "address_id": "222",
        "contact": "John Doe",
        "email": "john.doe@acme.com",
        "phone": "(111) 111-1111",
    },
    "disney_mail": {
        "address_id": "333",
        "contact": "Anthony Williams",
        "email": "anthony.williams@disney.com",
        "phone": "(222) 222-2222",
    },
}

LOCATIONS = {
    "building": {
        "loc_id": "DGSBM",
        "desc": "DGS - BUILDING MAINTENANCE",
    },
    "contract": {
        "loc_id": "DGSCM",
        "desc": "DGS - FACILITIES CONTRACT MAINTENANCE",
    },
    "energy": {
        "loc_id": "DGSEE",
        "desc": "DGS - ENERGY",
    },
    "fleet": {
        "loc_id": "DGSFM",
        "desc": "DGS - FLEET MANAGEMENT",
    },
    "dpw": {
        "loc_id": "DPWWM",
        "desc": "DPW - WASTE MANAGEMENT",
    },
}

PO_RECORDS = {
    # Blanket PO between Acme and DGS, status: Sent
    "po1": {
        "po_nbr": "P111",
        "release_nbr": 0,
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "status": "3PS",
        "agency": "DGS",
        "cost": 0.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["building"]["loc_id"],
    },
    # PO Release between Acme and DGS, status: Partial Receipt
    "po1_1": {
        "po_nbr": "P111",
        "release_nbr": 1,
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "status": "3PPR",
        "agency": "DGS",
        "cost": 75.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["fleet"]["loc_id"],
    },
    # PO Release between Acme and DPW, status: Partial Receipt
    # Excluded because it's a DPW release
    "po1_2": {
        "po_nbr": "P111",
        "release_nbr": 2,
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "status": "3PPR",
        "agency": "DPW",
        "cost": 20.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["dpw"]["loc_id"],
    },
    # Open Market PO between Disney and DGS, status: Closed
    # Excluded because it's closed
    "po2": {
        "po_nbr": "P222",
        "release_nbr": 0,
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "status": "3PCO",
        "agency": "DGS",
        "cost": 15.50,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["energy"]["loc_id"],
    },
    # Blanket PO between Disney and DPW, status: Sent
    # This is the PO for an Agency umbrella contract
    # which allows DGS to create releases off of it
    "po4": {
        "po_nbr": "P444",
        "release_nbr": 0,
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "status": "3PS",
        "agency": "DPW",
        "cost": 0.00,
        "date": datetime(2020, 7, 1),
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["dpw"]["loc_id"],
    },
    # PO Release between Disney and DGS, status: Partial Receipt
    "po4_1": {
        "po_nbr": "P444",
        "release_nbr": 1,
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "status": "3PPR",
        "agency": "DGS",
        "cost": 10.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["energy"]["loc_id"],
    },
    # Open Market PO between DGS and Acme, status: Sent
    "po5": {
        "po_nbr": "P555",
        "release_nbr": 0,
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "status": "3PS",
        "agency": "DGS",
        "cost": 20.00,
        "date": datetime(2020, 7, 1),
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["contract"]["loc_id"],
    },
    # Open Market PO between Acme and DPW, status: Sent
    # This PO is excluded because it isn't available to DGS
    "po6": {
        "po_nbr": "P666",
        "release_nbr": 0,
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "status": "3PS",
        "agency": "DPW",
        "cost": 20.00,
        "date": datetime(2020, 7, 1),
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["building"]["loc_id"],
    },
    # Blanket PO between Disney and DGS, status: Closed
    # This PO is excluded because it's closed
    "po7": {
        "po_nbr": "P777",
        "release_nbr": 0,
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "status": "3PCO",
        "agency": "DGS",
        "cost": 0.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "loc_id": LOCATIONS["fleet"]["loc_id"],
    },
}

CONTRACTS = {
    # Included in list of contracts
    "blanket1_DGS": {
        "po_nbr": PO_RECORDS["po1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1"]["release_nbr"],
        "contract_agency": "DGS",
        "start_date": datetime(2020, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 750.00,
        "dollar_spent": 50.00,
    },
    # Excluded because it's related to DPW
    "blanket1_DPW": {
        "po_nbr": PO_RECORDS["po1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1"]["release_nbr"],
        "contract_agency": "DPW",
        "start_date": datetime(2020, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 250.00,
        "dollar_spent": 50.00,
    },
    # Included because it's an Agency Umbrella contract
    "blanket4": {
        "po_nbr": PO_RECORDS["po4"]["po_nbr"],
        "release_nbr": PO_RECORDS["po4"]["release_nbr"],
        "contract_agency": "AGY",
        "start_date": datetime(2021, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 500.00,
        "dollar_spent": 10.00,
    },
    # Included in the list of contracts
    "blanket4_agy": {
        "po_nbr": PO_RECORDS["po4"]["po_nbr"],
        "release_nbr": PO_RECORDS["po4"]["release_nbr"],
        "contract_agency": "DGS",
        "start_date": datetime(2021, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 10000.00,
        "dollar_spent": 250.00,
    },
    # Excluded because it expired more than 90 days ago
    "blanket7": {
        "po_nbr": PO_RECORDS["po7"]["po_nbr"],
        "release_nbr": PO_RECORDS["po7"]["release_nbr"],
        "contract_agency": "DGS",
        "start_date": datetime(2010, 7, 1),
        "end_date": datetime(2020, 7, 1),
        "dollar_limit": 500.00,
        "dollar_spent": 20.00,
    },
}


INVOICES = {
    # Acme invoice for DGS, status: Paid
    # Excluded because it was paid more than 45 days ago
    "inv1": {
        "id": "invoice1",
        "po_nbr": PO_RECORDS["po1_1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1_1"]["release_nbr"],
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "invoice_nbr": "Invoice#1",
        "status": "4IP",
        "amount": 10.25,
        "invoice_date": datetime(2020, 8, 30),
        "modified": datetime(2020, 8, 30),
    },
    # Acme invoice for DGS, status: Paid
    # Included because it was paid less than 45 days ago
    "inv2": {
        "id": "invoice2",
        "po_nbr": PO_RECORDS["po1_1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1_1"]["release_nbr"],
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "invoice_nbr": "Invoice#2",
        "status": "4IP",
        "amount": 25.00,
        "invoice_date": datetime(2020, 7, 1),
        "modified": datetime(2050, 8, 30),
    },
    # Acme invoice for DGS, status: Approved for Payment
    # Included because it hasn't yet been paid
    "inv3": {
        "id": "invoice3",
        "po_nbr": PO_RECORDS["po1_1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1_1"]["release_nbr"],
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "invoice_nbr": "Invoice#3",
        "status": "4IA",
        "amount": 25.00,
        "invoice_date": datetime(2020, 7, 1),
        "modified": datetime(2020, 8, 30),
    },
    # Acme invoice for DPW, status: In Progress
    # Excluded because it's for DPW
    "inv4": {
        "id": "invoice4",
        "po_nbr": PO_RECORDS["po1_2"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1_2"]["release_nbr"],
        "vendor_id": VENDORS["acme"]["vendor_id"],
        "invoice_nbr": "Invoice#4",
        "status": "4II",
        "amount": 10.50,
        "invoice_date": datetime(2020, 8, 15),
        "modified": datetime(2020, 8, 30),
    },
    # Disney invoice for DGS, status: Approved for Payment
    # Included because it hasn't yet been paid
    "inv5": {
        "id": "invoice5",
        "po_nbr": PO_RECORDS["po2"]["po_nbr"],
        "release_nbr": PO_RECORDS["po2"]["release_nbr"],
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "invoice_nbr": "#1",
        "status": "4IA",
        "amount": 10.50,
        "invoice_date": datetime(2020, 9, 30),
        "modified": datetime(2020, 8, 30),
    },
    # Disney invoice for DGS, status: Cancelled
    # Included because it was canceled less than 45 days ago
    "inv6": {
        "id": "invoice6",
        "po_nbr": PO_RECORDS["po2"]["po_nbr"],
        "release_nbr": PO_RECORDS["po2"]["release_nbr"],
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "invoice_nbr": "#2",
        "status": "4IC",
        "amount": 5.00,
        "invoice_date": datetime(2020, 7, 1),
        "modified": datetime(2050, 8, 30),
    },
    # Disney invoice for DGS, status: Cancelled
    # Excluded because it was cancelled more than 45 days ago
    "inv7": {
        "id": "invoice7",
        "po_nbr": "P333",
        "release_nbr": 0,
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "invoice_nbr": "#3",
        "status": "4IC",
        "amount": 5.00,
        "invoice_date": datetime(2020, 7, 15),
        "modified": datetime(2020, 8, 30),
    },
    # Disney invoice for DGS, status: In Progress
    # Included because it hasn't yet been paid
    "inv8": {
        "id": "invoice8",
        "po_nbr": PO_RECORDS["po4_1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po4_1"]["release_nbr"],
        "vendor_id": VENDORS["disney"]["vendor_id"],
        "invoice_nbr": "#4",
        "status": "4II",
        "amount": 10.00,
        "invoice_date": datetime(2020, 8, 1),
        "modified": datetime(2020, 8, 30),
    },
}

INV_HISTORY = {
    "inv1_4IR": {
        "id": "update_1.1",
        "invoice_id": INVOICES["inv1"]["id"],
        "invoice_nbr": INVOICES["inv1"]["invoice_nbr"],
        "vendor_id": INVOICES["inv1"]["vendor_id"],
        "from_status": "4II",
        "to_status": "4IR",
        "status_date": datetime(2020, 8, 1),
    },
    "inv1_4IA": {
        "id": "update_1.2",
        "invoice_id": INVOICES["inv1"]["id"],
        "invoice_nbr": INVOICES["inv1"]["invoice_nbr"],
        "vendor_id": INVOICES["inv1"]["vendor_id"],
        "from_status": "4IR",
        "to_status": "4IA",
        "status_date": datetime(2020, 9, 1),
    },
    "inv1_4IP": {
        "id": "update_1.3",
        "invoice_id": INVOICES["inv1"]["id"],
        "invoice_nbr": INVOICES["inv1"]["invoice_nbr"],
        "vendor_id": INVOICES["inv1"]["vendor_id"],
        "from_status": "4IA",
        "to_status": "4IP",
        "status_date": datetime(2020, 10, 1),  # more than 45 days ago
    },
    "inv2_4IP": {
        "id": "update_2",
        "invoice_id": INVOICES["inv2"]["id"],
        "invoice_nbr": INVOICES["inv2"]["invoice_nbr"],
        "vendor_id": INVOICES["inv2"]["vendor_id"],
        "from_status": "4IA",
        "to_status": "4IP",
        "status_date": datetime(2025, 9, 1),  # less than 45 days ago
    },
    "inv3_4IA": {
        "id": "update_3",
        "invoice_id": INVOICES["inv3"]["id"],
        "invoice_nbr": INVOICES["inv3"]["invoice_nbr"],
        "vendor_id": INVOICES["inv3"]["vendor_id"],
        "from_status": "4IR",
        "to_status": "4IA",
        "status_date": datetime(2025, 9, 1),
    },
    "inv6_4IC": {
        "id": "update_6",
        "invoice_id": INVOICES["inv6"]["id"],
        "invoice_nbr": INVOICES["inv6"]["invoice_nbr"],
        "vendor_id": INVOICES["inv6"]["vendor_id"],
        "from_status": "4IC",
        "to_status": "4IC",
        "status_date": datetime(2025, 9, 1),  # less than 45 days ago
    },
    "inv7_4IC": {
        "id": "update_7",
        "invoice_id": INVOICES["inv7"]["id"],
        "invoice_nbr": INVOICES["inv7"]["invoice_nbr"],
        "vendor_id": INVOICES["inv7"]["vendor_id"],
        "from_status": "4IC",
        "to_status": "4IC",
        "status_date": datetime(2020, 9, 1),  # more than 45 days ago
    },
}


RECEIPTS = {
    "receipt1": {
        "receipt_id": "D001",
        "po_nbr": PO_RECORDS["po1_1"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1_1"]["release_nbr"],
        "status": "5CR",
        "owner": "JANEDOE",
        "loc_id": LOCATIONS["building"]["loc_id"],
        "desc": INVOICES["inv3"]["invoice_nbr"],
        "agency": "DGS",
        "created_date": datetime(2020, 9, 1),
        "modified_date": datetime(2025, 9, 1),
    },
    "receipt2": {
        "receipt_id": "D002",
        "po_nbr": PO_RECORDS["po1_2"]["po_nbr"],
        "release_nbr": PO_RECORDS["po1_2"]["release_nbr"],
        "status": "5CI",
        "owner": "JOHNSMITH",
        "loc_id": LOCATIONS["fleet"]["loc_id"],
        "desc": INVOICES["inv4"]["invoice_nbr"],
        "agency": "DGS",
        "created_date": datetime(2020, 9, 1),
        "modified_date": datetime(2025, 9, 1),
    },
    "receipt3": {
        "receipt_id": "D003",
        "po_nbr": PO_RECORDS["po2"]["po_nbr"],
        "release_nbr": PO_RECORDS["po2"]["release_nbr"],
        "status": "5CA",
        "owner": "JOHNDOE",
        "loc_id": LOCATIONS["building"]["loc_id"],
        "desc": INVOICES["inv5"]["invoice_nbr"],
        "agency": "DGS",
        "created_date": datetime(2020, 9, 1),
        "modified_date": datetime(2025, 9, 1),
    },
    "receipt4": {
        "receipt_id": "D004",
        "po_nbr": "P333",
        "release_nbr": 0,
        "status": "5CA",
        "owner": "JOHNDOE",
        "loc_id": LOCATIONS["building"]["loc_id"],
        "desc": INVOICES["inv7"]["invoice_nbr"],
        "agency": "DGS",
        "created_date": datetime(2020, 9, 1),
        "modified_date": datetime(2020, 9, 1),
    },
    "receipt5": {
        "receipt_id": "D005",
        "po_nbr": "P333",
        "release_nbr": 0,
        "status": "5CA",
        "owner": "JOHNDOE",
        "loc_id": LOCATIONS["building"]["loc_id"],
        "desc": INVOICES["inv7"]["invoice_nbr"],
        "agency": "DPW",
        "created_date": datetime(2020, 9, 1),
        "modified_date": datetime(2020, 9, 1),
    },
}


APPROVERS = {
    "approver1.1P": {
        "receipt_id": RECEIPTS["receipt1"]["receipt_id"],
        "approver_type": "P",
        "approver": "DONALDDUCK",
        "order": 1,
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "approval_date": None,
    },
    "approver1.2P": {
        "receipt_id": RECEIPTS["receipt1"]["receipt_id"],
        "approver_type": "P",
        "approver": "JOHNSMITH",
        "order": 2,
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "approval_date": None,
    },
    "approver2.1P": {
        "receipt_id": RECEIPTS["receipt2"]["receipt_id"],
        "approver_type": "P",
        "approver": "JOHNSMITH",
        "order": 2,
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "approval_date": None,
    },
    "approver2.1A": {
        "receipt_id": RECEIPTS["receipt2"]["receipt_id"],
        "approver_type": "A",
        "approver": "JANEDOE",
        "order": 2,
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "approval_date": None,
    },
    "approver3.1P": {
        "receipt_id": RECEIPTS["receipt3"]["receipt_id"],
        "approver_type": "P",
        "approver": "JOHNSMITH",
        "order": 2,
        "proxy_approver": "MICKEYMOUSE",
        "requested_date": datetime(2020, 9, 1),
        "approval_date": datetime(2025, 9, 1),
    },
    "approver4.1P": {
        "receipt_id": RECEIPTS["receipt4"]["receipt_id"],
        "approver_type": "P",
        "approver": "JANEDOE",
        "order": 1,
        "proxy_approver": "JOHNSMITH",
        "requested_date": datetime(2020, 9, 1),
        "approval_date": datetime(2020, 9, 1),
    },
}
