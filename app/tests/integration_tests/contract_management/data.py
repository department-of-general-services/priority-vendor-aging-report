from datetime import datetime

CITIBUY = {
    "po": {
        "Title": ["P111", "P111:2", "P111:3", "P333"],
        "PO Number": ["111", "111", "111", "333"],
        "Release Number": [0, 2, 3, 0],
        "Vendor ID": ["111", "111", "111", "333"],
        "Vendor": ["Acme", "Acme", "Acme", "Apple"],
        "Status": [
            "3PS - Sent",
            "3PPR - Partial Receipt",
            "3PPR - Partial Receipt",
            "3PS - Sent",
        ],
        "PO Type": ["Master Blanket", "Release", "Release", "Open Market"],
        "Actual Cost": [0, 150, 100, 25],
        "PO Date": [
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
        ],
        "Contract Dollar Limit": [0, 150, 100, None],
        "Contract Amount Spent": [0, 100, 80, None],
        "Contract Start Date": [
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            None,
        ],
        "Contract End Date": [
            datetime(2050, 7, 1),
            datetime(2050, 7, 1),
            datetime(2050, 7, 1),
            None,
        ],
    },
    "vendor": {
        "Title": ["Acme", "Apple"],
        "Vendor ID": ["111", "333"],
        "Point of Contact": ["Alice Williams", "Steve Jobs"],
        "Email": ["alice@acme.com", "steve@apple.com"],
        "Phone": ["111-111-1111", "333-333-3333"],
    },
}

SHAREPOINT = {
    "po": {
        "id": ["1", "2", "3", "4"],
        "Title": ["P111", "P111:1", "P111:2", "P222"],
        "PO Number": ["111", "111", "111", "222"],
        "Release Number": [0, 1, 2, 0],
        "PO Type": ["Master Blanket", "Release", "Release", "Open Market"],
        "Vendor ID": ["111", "111", "111", "222"],
        "Vendor": ["Acme", "Acme", "Acme", "Disney"],
        "Status": [
            "3PS - Sent",
            "3PPR - Partial Receipt",
            "3PI - In Progress",
            "3PS - Sent",
        ],
        "Actual Cost": [0, 150, 150, 40],
        "PO Date": [
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
        ],
        "Contract Dollar Limit": [0, 150, 150, None],
        "Contract Amount Spent": [0, 100, 100, None],
        "Contract Start Date": [
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            None,
        ],
        "Contract End Date": [
            datetime(2050, 7, 1),
            datetime(2050, 7, 1),
            datetime(2050, 7, 1),
            None,
        ],
    },
    "vendor": {
        "id": ["1", "2"],
        "@odata.etag": ["111", "222"],
        "Content Type": ["Item", "Item"],
        "Title": ["Acme", "Disney"],
        "Attachments": [None, None],
        "Point of Contact": ["John Doe", "Mickey Mouse"],
        "Email": ["john@acme.com", "mickey@disney.com"],
        "Phone": ["111-111-1111", "222-222-2222"],
        "Vendor ID": ["111", "222"],
    },
}
