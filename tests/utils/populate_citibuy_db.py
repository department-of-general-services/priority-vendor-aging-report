from __future__ import annotations

from sqlalchemy.orm import Session

from aging_report.citibuy.models import PurchaseOrder, Vendor

VENDORS = [
    {
        "id": "123",
        "name": "Acme",
        "contact": "Jane Doe",
        "email": "jane.doe@acme.com",
        "phone": "(123) 456-7890",
    }
]

POS = [{"po_number": "123", "release_number": 0, "vendor_id": "123"}]


def populate_db(session: Session) -> None:
    """Populates the mock database with test data

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture
    """
    vendors = [Vendor(**v) for v in VENDORS]
    pos = [PurchaseOrder(**po) for po in POS]
    for v in vendors:
        session.add(v)
    for po in pos:
        session.add(po)
    session.commit()
