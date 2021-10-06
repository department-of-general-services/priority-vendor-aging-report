from sqlalchemy import Column, Integer, String, ForeignKey

from aging_report.citibuy.models.base import Base


class PurchaseOrder(Base):
    """Table that contains summary level information about a Purchase Order"""

    __tablename__ = "PO_HEADER"

    # columns
    po_number = Column("PO_NBR", String, primary_key=True)
    release_number = Column("RELEASE_NBR", Integer, primary_key=True)
    vendor_id = Column("VEND_ID", String, ForeignKey("VENDOR.VENDOR_NBR"))
