import dgs_fiscal.systems.citibuy.models.base as db


class Vendor(db.Base):
    """Table that contains information about vendors"""

    __tablename__ = "VENDOR"

    # columns
    id = db.Column("VENDOR_NBR", db.String, primary_key=True)
    name = db.Column("NAME", db.String)
    contact = db.Column("EMA_CONTACT_NAME", db.String)
    email = db.Column("EMA_EMAIL", db.String)
    phone = db.Column("EMA_PHONE", db.String)

    # relationships
    purchase_orders = db.relationship("PurchaseOrder", backref="vendor")

    # column list for querying
    columns = ("name", "contact", "email", "phone")
