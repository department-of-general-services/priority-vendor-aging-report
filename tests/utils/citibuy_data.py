VENDORS = [
    {
        "id": "111",
        "name": "Acme",
        "contact": "Jane Doe",
        "email": "jane.doe@acme.com",
        "phone": "(111) 111-1111",
    },
    {
        "id": "222",
        "name": "Disney",
        "contact": "Anthony Williams",
        "email": "anthony.williams@disney.com",
        "phone": "(222) 222-2222",
    },
]

PURCHASE_ORDERS = [
    {
        "po_number": "111",
        "release_number": 0,
        "vendor_id": "111",
        "status": "3PS",
        "agency": "DGS",
        "cost": None,
        "date": None,
    },
    {
        "po_number": "111",
        "release_number": 1,
        "vendor_id": "111",
        "status": "3PPR",
        "agency": "DGS",
        "cost": 75.00,
        "date": None,
    },
    {
        "po_number": "222",
        "release_number": 0,
        "vendor_id": "222",
        "status": "3PCO",
        "agency": "DGS",
        "cost": 15.50,
        "date": None,
    },
    {
        "po_number": "333",
        "release_number": 0,
        "vendor_id": "222",
        "status": "3PPR",
        "agency": "AGY",
        "cost": 20.00,
        "date": None,
    },
]

INVOICES = [
    {
        "id": "invoice1",
        "po_number": "111",
        "release_number": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#1",
        "status": "4IP",
        "amount": 10.25,
        "invoice_date": None,
    },
    {
        "id": "invoice2",
        "po_number": "111",
        "release_number": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#2",
        "status": "4IP",
        "amount": 25.00,
        "invoice_date": None,
    },
    {
        "id": "invoice3",
        "po_number": "111",
        "release_number": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#2",
        "status": "4IA",
        "amount": 25.00,
        "invoice_date": None,
    },
    {
        "id": "invoice4",
        "po_number": "111",
        "release_number": 1,
        "vendor_id": "111",
        "invoice_number": "Invoice#3",
        "status": "4II",
        "amount": 10.50,
        "invoice_date": None,
    },
    {
        "id": "invoice5",
        "po_number": "222",
        "release_number": 0,
        "vendor_id": "222",
        "invoice_number": "#1",
        "status": "4IP",
        "amount": 10.50,
        "invoice_date": None,
    },
    {
        "id": "invoice6",
        "po_number": "222",
        "release_number": 0,
        "vendor_id": "222",
        "invoice_number": "#2",
        "status": "4IP",
        "amount": 5.00,
        "invoice_date": None,
    },
    {
        "id": "invoice7",
        "po_number": "333",
        "release_number": 0,
        "vendor_id": "222",
        "invoice_number": "#3",
        "status": "4IP",
        "amount": 5.00,
        "invoice_date": None,
    },
]

BLANKET_CONTRACTS = [
    {
        "po_number": "111",
        "release_number": 0,
        "agency": "DGS",
        "start_date": None,
        "end_date": None,
        "dollar_limit": 1000.00,
        "dollar_spent": 50.00,
    },
]
