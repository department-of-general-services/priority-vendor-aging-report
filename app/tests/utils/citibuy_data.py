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
        "vendor_id": "111",
        "address_id": "111",
        "address_type": "M",
        "default": "Y",
    },
    "acme_extra": {
        "vendor_id": "111",
        "address_id": "222",
        "address_type": "R",
        "default": "Y",
    },
    "disney": {
        "vendor_id": "222",
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

PO_RECORDS = {
    # Blanket PO between Acme and DGS, status: Sent
    "po1": {
        "po_nbr": "P111",
        "release_nbr": 0,
        "vendor_id": "111",
        "status": "3PS",
        "agency": "DGS",
        "cost": 0.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # PO Release between Acme and DGS, status: Partial Receipt
    "po1_1": {
        "po_nbr": "P111",
        "release_nbr": 1,
        "vendor_id": "111",
        "status": "3PPR",
        "agency": "DGS",
        "cost": 75.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # PO Release between Acme and DPW, status: Partial Receipt
    # Excluded because it's a DPW release
    "po1_2": {
        "po_nbr": "P111",
        "release_nbr": 2,
        "vendor_id": "222",
        "status": "3PPR",
        "agency": "DPW",
        "cost": 20.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # Open Market PO between Disney and DGS, status: Closed
    # Excluded because it's closed
    "po2": {
        "po_nbr": "P222",
        "release_nbr": 0,
        "vendor_id": "222",
        "status": "3PCO",
        "agency": "DGS",
        "cost": 15.50,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # Blanket PO between Disney and DPW, status: Sent
    # This is the PO for an Agency umbrella contract
    # which allows DGS to create releases off of it
    "po4": {
        "po_nbr": "P444",
        "release_nbr": 0,
        "vendor_id": "222",
        "status": "3PS",
        "agency": "DPW",
        "cost": 0.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # PO Release between Disney and DGS, status: Partial Receipt
    "po4_1": {
        "po_nbr": "P444",
        "release_nbr": 1,
        "vendor_id": "222",
        "status": "3PPR",
        "agency": "DGS",
        "cost": 10.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # Open Market PO between DGS and Disney, status: Sent
    "po5": {
        "po_nbr": "P555",
        "release_nbr": 0,
        "vendor_id": "111",
        "status": "3PS",
        "agency": "DGS",
        "cost": 20.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # Open Market PO between Disney and DPW, status: Sent
    # This PO is excluded because it isn't available to DGS
    "po6": {
        "po_nbr": "P666",
        "release_nbr": 0,
        "vendor_id": "111",
        "status": "3PS",
        "agency": "DPW",
        "cost": 20.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
    # Blanket PO between Disney and DGS, status: Closed
    # This PO is excluded because it's closed
    "po7": {
        "po_nbr": "P777",
        "release_nbr": 0,
        "vendor_id": "222",
        "status": "3PCO",
        "agency": "DGS",
        "cost": 0.00,
        "date": None,
        "buyer": "JOHNSMITH",
        "desc": "description",
        "location": "DGS",
    },
}

INVOICES = {
    # Acme invoice for DGS, status: Paid
    "inv1": {
        "id": "invoice1",
        "po_nbr": "P111",
        "release_nbr": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#1",
        "status": "4IP",
        "amount": 10.25,
        "invoice_date": datetime(2020, 8, 30),
    },
    # Acme invoice for DGS, status: Paid
    "inv2": {
        "id": "invoice2",
        "po_nbr": "P111",
        "release_nbr": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#2",
        "status": "4IP",
        "amount": 25.00,
        "invoice_date": datetime(2020, 7, 1),
    },
    # Acme invoice for DGS, status: In
    "inv3": {
        "id": "invoice3",
        "po_nbr": "P111",
        "release_nbr": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#2",
        "status": "4IA",
        "amount": 25.00,
        "invoice_date": datetime(2020, 7, 1),
    },
    # Acme invoice for DPW, status: In Progress
    # Excluded because it's for DPW
    "inv4": {
        "id": "invoice4",
        "po_nbr": "P111",
        "release_nbr": 2,
        "vendor_id": "111",
        "invoice_number": "Invoice#3",
        "status": "4II",
        "amount": 10.50,
        "invoice_date": datetime(2020, 8, 15),
    },
    # Disney invoice for DGS, status: Approved for Payment
    "disney_inv5": {
        "id": "invoice5",
        "po_nbr": "P222",
        "release_nbr": 0,
        "vendor_id": "222",
        "invoice_number": "#1",
        "status": "4IA",
        "amount": 10.50,
        "invoice_date": datetime(2020, 9, 30),
    },
    # Disney invoice for DGS, status: Cancelled
    "disney_inv6": {
        "id": "invoice6",
        "po_nbr": "P222",
        "release_nbr": 0,
        "vendor_id": "222",
        "invoice_number": "#2",
        "status": "4IC",
        "amount": 5.00,
        "invoice_date": datetime(2020, 7, 1),
    },
    # Disney invoice for DGS, status: In Progress
    "disney_inv7": {
        "id": "invoice7",
        "po_nbr": "P333",
        "release_nbr": 0,
        "vendor_id": "222",
        "invoice_number": "#3",
        "status": "4II",
        "amount": 5.00,
        "invoice_date": datetime(2020, 7, 15),
    },
    # Disney invoice for DGS, status: In Progress
    "disney_inv8": {
        "id": "invoice8",
        "po_nbr": "P444",
        "release_nbr": 1,
        "vendor_id": "222",
        "invoice_number": "#4",
        "status": "4IP",
        "amount": 10.00,
        "invoice_date": datetime(2020, 8, 1),
    },
}

CONTRACTS = {
    "blanket1_DGS": {
        "po_nbr": "P111",
        "release_nbr": 0,
        "contract_agency": "DGS",
        "start_date": datetime(2020, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 750.00,
        "dollar_spent": 50.00,
    },
    "blanket1_DPW": {
        "po_nbr": "P111",
        "release_nbr": 0,
        "contract_agency": "DPW",
        "start_date": datetime(2020, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 250.00,
        "dollar_spent": 50.00,
    },
    "blanket4": {
        "po_nbr": "P444",
        "release_nbr": 0,
        "contract_agency": "AGY",
        "start_date": datetime(2021, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 500.00,
        "dollar_spent": 10.00,
    },
    "blanket4_agy": {
        "po_nbr": "P444",
        "release_nbr": 0,
        "contract_agency": "DGS",
        "start_date": datetime(2021, 7, 1),
        "end_date": datetime(2050, 7, 1),
        "dollar_limit": 10000.00,
        "dollar_spent": 250.00,
    },
    "blanket7": {
        "po_nbr": "P777",
        "release_nbr": 0,
        "contract_agency": "DGS",
        "start_date": datetime(2010, 7, 1),
        "end_date": datetime(2020, 7, 1),
        "dollar_limit": 500.00,
        "dollar_spent": 20.00,
    },
}
