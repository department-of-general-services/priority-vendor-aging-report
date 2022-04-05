from pandas import Timestamp

REPORT = {
    "Invoice Key": [
        "Invoice#2",
        "Invoice#3",
        "Invoice#6",
        "#1",
        "#2",
        "#4",
        "5",
    ],
    "Invoice": [
        "Invoice#2",
        "Invoice#3",
        "Invoice#6",
        "#1",
        "#2",
        "#4",
        "5",
    ],
    "WO": ["101", "102", "103", "201", "202", "203", "204"],
    "Invoice Date": [
        Timestamp("2020-07-01 00:00:00"),
        Timestamp("2020-07-01 00:00:00"),
        Timestamp("2022-09-30 00:00:00"),
        Timestamp("2020-09-30 00:00:00"),
        Timestamp("2020-07-01 00:00:00"),
        Timestamp("2020-08-01 00:00:00"),
        Timestamp("2022-09-30 00:00:00"),
    ],
    "Vendor": ["Acme", "Acme", "Acme", "Disney", "Disney", "Disney", "Disney"],
    "Vendor ID": ["111", "111", "111", "222", "222", "222", "222"],
    "Amount": [2385.08, 273.16, 413.82, 1429.08, 273.16, 170.73, 136.58],
    "Days Outsatnding": [966, 960, 923, 903, 903, 888, 851],
    "PO: Release": [
        "P111:1",
        "P111:1",
        "P999",
        "P222",
        "P222",
        "P444:1",
        "P444:1",
    ],
}

OUTPUT = {
    **REPORT,
    "CitiBuy Status": [
        "4IP - Paid",
        "4IA - Approved for Payment",
        "",
        "4IA - Approved for Payment",
        "4IC - Cancelled",
        "4II - In Progress",
        "",
    ],
}
