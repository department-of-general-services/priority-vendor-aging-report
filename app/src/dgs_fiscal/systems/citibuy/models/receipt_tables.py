import dgs_fiscal.systems.citibuy.models.base as db


class Receipt(db.Base):
    """Stores summary level information about the receipts for an invoice"""

    __tablename__ = "RECEIPT_HEADER"
    __table_args__ = (db.init_po_joint_key(),)

    # columns
    receipt_id = db.Column("RECEIPT_ID", db.String, primary_key=True)
    po_nbr = db.Column("PO_NBR", db.String)
    release_nbr = db.Column("RELEASE_NBR", db.Integer)
    status = db.Column("CURRENT_HEADER_STATUS", db.String)
    owner = db.Column("RECEIPT_OWNER_ID", db.String)
    location = db.Column("LOCATION", db.String)
    desc = db.Column("SHORT_DESC", db.String)
    agency = db.Column("DEPT_NBR_PREFIX", db.String)
    receipt_date = db.Column("RECEIPT_DATE", db.DateTime)
    created_date = db.Column("DATE_CREATED", db.DateTime)

    # relationships
    approvers = db.relationship("Approver", backref="location")


class Approver(db.Base):
    """Stores information about users in the approval path for a receipt"""

    __tablename__ = "RECEIPT_ROUTING"

    # columns
    receipt_id = db.Column(
        "RECEIPT_ID",
        db.String,
        db.ForeignKey("RECEIPT_HEADER.RECEIPT_ID"),
        primary_key=True,
    )
    approver_type = db.Column(
        "RECEIPT_APPROVER_TYPE",
        db.String,
        primary_key=True,
    )
    approver = db.Column("RECEIPT_APPROVER", db.String, primary_key=True)
    order = db.Column("ORDER_SEQUENCE", db.Integer, primary_key=True)
    proxy_approver = db.Column("PROXY_USER_ID", db.String)
    requested_date = db.Column("RECEIT_REQ_APP_DATE", db.DateTime)
