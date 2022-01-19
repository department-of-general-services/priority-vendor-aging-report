import dgs_fiscal.systems.citibuy.models.base as db


class Invoice(db.Base):
    """Table that contains summary level information about an Invoice"""

    __tablename__ = "INVOICE_HDR"
    __table_args__ = (db.init_po_joint_key(),)

    # columns
    id = db.Column("ID", db.String, primary_key=True)
    po_nbr = db.Column("PO_NBR", db.String)
    release_nbr = db.Column("RELEASE_NBR", db.Integer)
    invoice_nbr = db.Column("INVOICE_NBR", db.String)
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
    status_history = db.relationship("InvoiceStatusHistory", backref="invoice")


class InvoiceStatusHistory(db.Base):
    """Table that records time stamps of each invoice's previous statuses"""

    __tablename__ = "INVOICE_STATUS_DATES"

    # column
    id = db.Column("ID", db.String, primary_key=True)
    invoice_nbr = db.Column("INVOIC_NBR", db.String)
    vendor_id = db.Column("VENDOR_NBR", db.String)
    from_status = db.Column("FROM_STATUS", db.String)
    to_status = db.Column("TO_STATUS", db.String)
    status_date = db.Column("INVOICE_STATUS_DATE", db.DateTime)
    invoice_id = db.Column(
        "HEADER_ID",
        db.String,
        db.ForeignKey("INVOICE_HDR.ID"),
    )
