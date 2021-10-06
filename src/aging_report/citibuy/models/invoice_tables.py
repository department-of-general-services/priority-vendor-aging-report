from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
)

from aging_report.citibuy.models.base import Base


class Invoice(Base):
    """Table that contains summary level information about an Invoice"""

    __tablename__ = "INVOICE_HDR"

    # columns
    id = Column("ID", String, primary_key=True)
    po_number = Column("PO_NBR", String)
    release_number = Column("RELEASE_NBR", Integer)
    vendor_id = Column("VENDOR_NBR", String, ForeignKey("VENDOR.VENDOR_NBR"))
    invoice_number = Column("INVOICE_NBR", String)
    status = Column("INVOICE_STATUS", String)
    amount = Column("INVOICE_AMT", Float(asdecimal=True))
    __table_args__ = (
        ForeignKeyConstraint(
            ["PO_NBR", "RELEASE_NBR"],  # Invoice cols
            ["PO_HEADER.PO_NBR", "PO_HEADER.RELEASE_NBR"],  # PO cols
        ),
    )

    # relationship
    purchase_order = relationship("Vendor", backref="invoices")
