from datetime import datetime

import numpy as np

CITIBUY = {
    "po": {
        "Title": ["P111", "P111:2", "P111:3", "P333", "P444"],
        "PO Number": ["P111", "P111", "P111", "P333", "P444"],
        "Release Number": [0, 2, 3, 0, 0],
        "PO Type": [
            "Master Blanket",
            "Release",
            "Release",
            "Open Market",
            "Master Blanket",
        ],
        "Vendor": ["111", "111", "111", "333", "333"],
        "Status": [
            "3PS - Sent",
            "3PPR - Partial Receipt",
            "3PPR - Partial Receipt",
            "3PS - Sent",
            "3PS - Sent",
        ],
        "Actual Cost": [0, 150, 100, 25, 0],
        "PO Date": [
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            datetime(2020, 7, 1),
            None,
        ],
    },
    "vendor": {
        "Title": ["Acme", "Disney", "Apple"],
        "Vendor ID": ["111", "222", "333"],
        "Point of Contact": ["Alice Williams", "Mickey Mouse", "Steve Jobs"],
        "Email": ["alice@acme.com", "mickey@disney.com", "steve@apple.com"],
        "Phone": ["111-111-1111", "222-222-2222", "333-333-3333"],
        "Emergency Contact": ["", "", ""],
        "Emergency Phone": ["", "", ""],
        "Emergency Email": ["", "", ""],
    },
    "contract": {
        "Title": ["P111", "P333"],
        "Dollar Limit": [150, 200],
        "Amount Spent": [125, 0],
        "Start Date": [datetime(2020, 7, 1), datetime(2020, 7, 1)],
        "End Date": [datetime(2050, 7, 1), datetime(2050, 7, 1)],
        "Vendor": ["111", "333"],
    },
}

SHAREPOINT = {
    "po": {
        "id": ["1", "2", "3", "4"],
        "Title": ["P111", "P111:1", "P111:2", "P222"],
        "PO Number": ["111", "111", "111", "222"],
        "Release Number": [0, 1, 2, 0],
        "PO Type": ["Master Blanket", "Release", "Release", "Master Blanket"],
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
        "Emergency Contact": [np.nan, np.nan],
        "Emergency Phone": [np.nan, np.nan],
        "Emergency Email": [np.nan, np.nan],
    },
    "contract": {
        "id": ["1", "2"],
        "Title": ["P111", "P222"],
        "Dollar Limit": [150, 100],
        "Amount Spent": [100, 100],
        "Start Date": [datetime(2020, 7, 1), None],
        "End Date": [datetime(2050, 7, 1), datetime(2050, 7, 1)],
        "Vendor": ["Acme", "Disney"],
    },
}
