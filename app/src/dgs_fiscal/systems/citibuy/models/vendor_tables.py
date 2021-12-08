import dgs_fiscal.systems.citibuy.models.base as db


class Vendor(db.Base):
    """Table that contains information about vendors"""

    __tablename__ = "VENDOR"

    # columns
    vendor_id = db.Column("VENDOR_NBR", db.String, primary_key=True)
    name = db.Column("NAME", db.String)
    emg_contact = db.Column("EMA_CONTACT_NAME", db.String)
    emg_email = db.Column("EMA_EMAIL", db.String)
    emg_phone = db.Column("EMA_PHONE", db.String)

    # relationships
    purchase_orders = db.relationship("PurchaseOrder", backref="vendor")

    # column list for querying
    columns = ("name", "emg_contact", "emg_email", "emg_phone")


class VendorAddress(db.Base):
    """Association table between Vendor and Address"""

    __tablename__ = "VENDOR_ADDRESS"

    # columns
    address_id = db.Column(
        "ADDR_ID",
        db.String,
        db.ForeignKey("ADDRESS.ADDR_ID"),
        primary_key=True,
    )
    vendor_id = db.Column(
        "VENDOR_NBR",
        db.String,
        db.ForeignKey("VENDOR.VENDOR_NBR"),
        primary_key=True,
    )
    address_type = db.Column("ADDRESS_TYPE_REF", db.String, primary_key=True)
    default = db.Column("DEFAULT_ADDRESS_FOR_TYPE", db.String)

    # relationships
    vendor = db.relationship("Vendor", backref="addresses")
    address = db.relationship("Address", backref="vendor")


class Address(db.Base):
    """Table that stores the mailing addresses for Vendors"""

    __tablename__ = "ADDRESS"

    # columns
    address_id = db.Column("ADDR_ID", db.String, primary_key=True)
    contact = db.Column("CONTACT", db.String)
    phone = db.Column("PH_NBR", db.String)
    email = db.Column("INTERNET_ADDRESS", db.String)
