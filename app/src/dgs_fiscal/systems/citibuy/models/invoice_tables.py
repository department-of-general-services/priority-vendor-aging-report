import dgs_fiscal.systems.citibuy.models.base as db


class Invoice(db.Base):
    """Table that contains summary level information about an Invoice"""

    __tablename__ = "INVOICE_HDR"
    __table_args__ = (db.init_po_joint_key(),)

    # columns
    id = db.Column("ID", db.String, primary_key=True)
    po_nbr = db.Column("PO_NBR", db.String)
    release_nbr = db.Column("RELEASE_NBR", db.Integer)
    invoice_number = db.Column("INVOICE_NBR", db.String)
    invoice_date = db.Column("INVOICE_DATE", db.DateTime)
    status = db.Column("INVOICE_STATUS", db.String)
    amount = db.Column("INVOICE_AMT", db.Float(asdecimal=True))
    vendor_id = db.Column(
        "VENDOR_NBR",
        db.String,
        db.ForeignKey("VENDOR.VENDOR_NBR"),
    )

    # relationship
    purchase_order = db.relationship("Vendor", backref="invoices")
