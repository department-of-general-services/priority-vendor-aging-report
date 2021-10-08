import aging_report.citibuy.models.base as db


class PurchaseOrder(db.Base):
    """Table that contains summary level information about a Purchase Order"""

    __tablename__ = "PO_HEADER"

    # columns
    po_number = db.Column("PO_NBR", db.String, primary_key=True)
    release_number = db.Column("RELEASE_NBR", db.Integer, primary_key=True)
    agency = db.Column("DEPT_NBR_PREFIX_REF", db.String)
    status = db.Column("CURRENT_HDR_STATUS", db.String)
    date = db.Column("PO_DATE", db.DateTime)
    cost = db.Column("ACTUAL_COST", db.Float(asdecimal=True))
    vendor_id = db.Column(
        "VEND_ID",
        db.String,
        db.ForeignKey("VENDOR.VENDOR_NBR"),
    )


class BlanketContract(db.Base):
    """Table that contains details about the blanket contract for the PO"""

    __tablename__ = "BLANKET_CONTROL"
    __table_args__ = (db.init_po_joint_key(),)

    # columns
    po_number = db.Column("PO_NBR", db.String, primary_key=True)
    release_number = db.Column("RELEASE_NBR", db.Integer, primary_key=True)
    agency = db.Column("DEPT_NBR_PREFIX", db.String, primary_key=True)
    start_date = db.Column("BLANKET_BEG_DATE", db.DateTime)
    end_date = db.Column("BLANKET_END_DATE", db.DateTime)
    dollar_limit = db.Column("BLANKET_DOLLAR_LIMIT", db.Float(asdecimal=True))
    dollar_spent = db.Column("BLANKET_DOLLAR_TODATE", db.Float(asdecimal=True))
