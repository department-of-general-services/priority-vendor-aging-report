NEW_REPORT = {
    "dtypes": {
        "Execution ID": "string",
        "Location": "string",
        "Status Age (days)": "int64",
        "Days Since Creation": "int64",
        "Status": "string",
        "Amount": "float64",
        "Document Type": "string",
        "Name": "string",
        # "Creation Date": "datetime64",
        "Vendor ID": "string",
        "Vendor Name": "string",
        "Document Number": "string",
        "Document Date": "datetime64",
        "PO Number": "string",
        "EA Number": "string",
        "Note": "string",
    },
    "columns": {
        "PO Number": "PO Number",
        "Vendor ID": "Vendor ID",
        "Vendor Name": "Vendor Name",
        "Document Number": "Document Number",
        "Document Date": "Invoice Date",
        "Amount": "Invoice Amount",
        "Status Age (days)": "Status Age (days)",
        "Days Since Creation": "Days Since Creation",
        "Execution ID": "Execution ID (Core)",
        "Location": "Location (Core)",
        "Creation Date": "Creation Date (Core)",
        "Assigned Date (Core)": "Assigned Date (Core)",
        "Name": "DGS Name",
    },
}

OLD_REPORT = {
    "dtypes": {
        "Document Number": "string",
        "Vendor ID": "string",
        "Comments": "string",
        "Current Status": "string",
        "Date of Most Recent Action": "datetime64[ns]",
        "Division": "object",
    }
}


DIVISIONS = {
    "Fleet": [
        "Donna Howard",
        "Donna Jones",
        "Erlynda Parton",
        "Jacquelyn Powers",
        "Jennifer Millan",
        "Keith Davis",
        "Lakia Carrillo",
        "Latrice Thomas",
        "Rosa Gold",
        "Abrar Abukhdeir",
        "Asia Ali",
        "David Gold",
    ],
    "Fiscal": [
        "Garrett Knight",
        "Rose Carter",
        "Benjamin Brosch",
        "Troy Parrish",
        "Tonay Davis",
        "Jonae Barnes",
        "Krystal Roberts-Saunders",
    ],
    "Facilities": [
        "Darryl Ragin",
        "Jim Fisher",
        "Phillip Waclawski",
        "Richard Nelson",
        "Karl Rusk",
        "Jason Ludd",
    ],
}


VALIDATION = [
    "Receipted",
    "errors",
    "Awaiting FMD/ Fleet Approval",
    "Funds Needed",
    "Change Order Requested",
    "other",
    "Credit Memo",
    "Justification",
    "Paid",
    "Reassign",
    "Duplicate",
]
