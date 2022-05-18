from datetime import datetime

import pandas as pd

from dgs_fiscal.etl.prompt_payment.constants import DIVISIONS


def compute_age_of_invoice(df: pd.DataFrame) -> pd.Series:
    """Calculates 'Age of Invoice' field"""
    now = datetime.now().date()
    age_of_invoice = now - df["Invoice Date"].dt.date
    return age_of_invoice


def compute_days_outstanding(df: pd.DataFrame) -> pd.Series:
    """Calculates 'Days Outstanding' field"""
    bins = [0, 30, 60, 90, 120, 10000]
    labels = [
        "Less than 30",
        "30 to 60 days",
        "60 to 90 days",
        "90 to 120 days",
        "Over 120 days",
    ]
    col = df["Days Since Creation"]
    days_outstanding = pd.cut(col, bins, False, labels)
    return days_outstanding


def compute_days_with_baps(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates 'Days with BAPS' field"""
    bins = [0, 10, 10000]
    labels = [
        "less than 10 days",
        "at least 10 days",
    ]
    col = df["Days Since Creation"] - df["Status Age (days)"]
    days_with_baps = pd.cut(col, bins, False, labels)
    return days_with_baps


def update_division(  # pylint: disable=dangerous-default-value
    df: pd.DataFrame,
    staff_mapping: list = DIVISIONS,
) -> pd.DataFrame:
    """Assigns the division associated with a give AP staff"""

    # change default to "No matching division"
    df["Division"] = "No matching division"

    # update rows that have multiple people listed
    multiples = df["DGS Name"].str.contains(",")
    df.loc[multiples, "Division"] = "Multiple people listed"

    # update remaining rows based on staff mapping
    for division, names in staff_mapping.items():
        staff = df["DGS Name"].isin(names)
        df.loc[staff, "Division"] = division

    return df
