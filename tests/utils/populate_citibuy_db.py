from __future__ import annotations
from typing import Iterable

from sqlalchemy.orm import Session

from aging_report.citibuy import models
from tests.utils import citibuy_data as data


def add_to_session(session: Session, entries: Iterable) -> None:
    """Adds uncommitted schema objects to the session

    Parameters
    ----------
    session: Session
        The SQLAlchemy session to add the items to before committing
    entries: Iterable
        An iterable of instances of SQLAlchemy models to add to the session
    """
    for entry in entries:
        session.add(entry)


def populate_db(session: Session) -> None:
    """Populates the mock database with test data

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture
    """
    vendors = [models.Vendor(**vendor) for vendor in data.VENDORS]
    pos = [models.PurchaseOrder(**po) for po in data.PURCHASE_ORDERS]
    invoices = [models.Invoice(**invoice) for invoice in data.INVOICES]
    contracts = [models.BlanketContract(**c) for c in data.BLANKET_CONTRACTS]
    add_to_session(session, vendors)
    add_to_session(session, pos)
    add_to_session(session, invoices)
    add_to_session(session, contracts)
    session.commit()
