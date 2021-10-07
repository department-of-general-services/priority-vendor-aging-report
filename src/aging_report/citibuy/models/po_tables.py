import aging_report.citibuy.models.base as db


class PurchaseOrder(db.Base):
    """Table that contains summary level information about a Purchase Order"""

    __tablename__ = "PO_HEADER"

    # columns
    po_number = db.Column("PO_NBR", db.String, primary_key=True)
    release_number = db.Column("RELEASE_NBR", db.Integer, primary_key=True)
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
    department = db.Column("DEPT_NBR_PREFIX", db.String)
    start_date = db.Column("BLANKET_BEG_DATE", db.DateTime)
    end_date = db.Column("BLANKET_END_DATE", db.DateTime)
