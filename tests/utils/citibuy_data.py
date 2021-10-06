VENDORS = [
    {
        "id": "123",
        "name": "Acme",
        "contact": "Jane Doe",
        "email": "jane.doe@acme.com",
        "phone": "(123) 456-7890",
    },
]

PURCHASE_ORDERS = [
    {"po_number": "123", "release_number": 0, "vendor_id": "123"},
]

INVOICES = [
    {
        "id": "invoice1",
        "po_number": "123",
        "release_number": 0,
        "vendor_id": "123",
        "invoice_number": "Invoice#1",
        "status": "4IP",
        "amount": 10.25,
    },
]
