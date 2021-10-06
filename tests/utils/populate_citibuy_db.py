from __future__ import annotations
from typing import Iterable

from sqlalchemy.orm import Session

from aging_report.citibuy.models import Invoice, PurchaseOrder, Vendor
from tests.utils import citibuy_data as data


def add_to_session(session: Session, entries: Iterable) -> None:
    """Adds uncommitted schema objects to the session"""
    for entry in entries:
        session.add(entry)


def populate_db(session: Session) -> None:
    """Populates the mock database with test data

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture
    """
    vendors = [Vendor(**vendor) for vendor in data.VENDORS]
    pos = [PurchaseOrder(**po) for po in data.PURCHASE_ORDERS]
    invoices = [Invoice(**invoice) for invoice in data.INVOICES]
    add_to_session(session, vendors)
    add_to_session(session, pos)
    add_to_session(session, invoices)
    session.commit()
