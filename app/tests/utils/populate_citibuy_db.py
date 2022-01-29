from __future__ import annotations
from typing import Iterable

from sqlalchemy.orm import Session

from dgs_fiscal.systems.citibuy import models
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


def create_records(model: models.Base, records: dict):
    """Uses a SQLAlchemy model to create a record for each entry in the data

    Parameters
    ----------
    model: models.Base
        A model that inherits from SQLAlchemy's declarative base
    records: dict
        A dictionary of entries to insert into the test database
    """
    return [model(**entry) for entry in records.values()]


def populate_db(session: Session) -> None:
    """Populates the mock database with test data

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture
    """
    vendors = create_records(models.Vendor, data.VENDORS)
    po_records = create_records(models.PurchaseOrder, data.PO_RECORDS)
    invoices = create_records(models.Invoice, data.INVOICES)
    contracts = create_records(models.BlanketContract, data.CONTRACTS)
    addresses = create_records(models.Address, data.ADDRESSES)
    locations = create_records(models.Location, data.LOCATIONS)
    ven_addresses = create_records(models.VendorAddress, data.VEN_ADDRESS)
    inv_history = create_records(models.InvoiceStatusHistory, data.INV_HISTORY)

    add_to_session(session, vendors)
    add_to_session(session, po_records)
    add_to_session(session, invoices)
    add_to_session(session, contracts)
    add_to_session(session, addresses)
    add_to_session(session, locations)
    add_to_session(session, ven_addresses)
    add_to_session(session, inv_history)
    session.commit()
