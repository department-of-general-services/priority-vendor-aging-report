from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

from aging_report.citibuy.models.base import Base


class Vendor(Base):
    """Table that contains information about vendors"""

    __tablename__ = "VENDOR"

    # columns
    id = Column("VENDOR_NBR", String, primary_key=True)
    name = Column("NAME", String)
    contact = Column("EMA_CONTACT_NAME", String)
    email = Column("EMA_EMAIL", String)
    phone = Column("EMA_PHONE", String)

    # relationships
    purchase_orders = relationship("PurchaseOrder", backref="vendor")
