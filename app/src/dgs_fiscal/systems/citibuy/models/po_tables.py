import dgs_fiscal.systems.citibuy.models.base as db


class Location(db.Base):
    """Provides the longer description for the PO location, which is the
    agency section or division associated with that Purchase Order
    """

    __tablename__ = "LOCATION"

    # columns
    loc_id = db.Column("LOCATION_NBR", db.String, primary_key=True)
    desc = db.Column("DESC_TEXT", db.String)

    # relationship
    purchase_orders = db.relationship("PurchaseOrder", backref="location")


class PurchaseOrder(db.Base):
    """Table that contains summary level information about a Purchase Order"""

    __tablename__ = "PO_HEADER"

    # columns
    po_nbr = db.Column("PO_NBR", db.String, primary_key=True)
    release_nbr = db.Column("RELEASE_NBR", db.Integer, primary_key=True)
    agency = db.Column("DEPT_NBR_PREFIX_REF", db.String)
    status = db.Column("CURRENT_HDR_STATUS", db.String)
    date = db.Column("PO_DATE", db.DateTime)
    cost = db.Column("ACTUAL_COST", db.Float(precision=2))
    desc = db.Column("SHORT_DESC", db.String)
    buyer = db.Column("PURCHASER", db.String)
    loc_id = db.Column(
        "LOC_ID",
        db.String,
        db.ForeignKey("LOCATION.LOCATION_NBR"),
    )
    vendor_id = db.Column(
        "VEND_ID",
        db.String,
        db.ForeignKey("VENDOR.VENDOR_NBR"),
    )

    # column list for querying
    columns = (
        "po_nbr",
        "release_nbr",
        "agency",
        "status",
        "date",
        "cost",
        "vendor_id",
        "desc",
        "loc_id",
        "buyer",
    )


class BlanketContract(db.Base):
    """Table that contains details about the blanket contract for the PO"""

    __tablename__ = "BLANKET_CONTROL"
    __table_args__ = (db.init_po_joint_key(),)

    # columns
    po_nbr = db.Column("PO_NBR", db.String, primary_key=True)
    release_nbr = db.Column("RELEASE_NBR", db.Integer, primary_key=True)
    contract_agency = db.Column("DEPT_NBR_PRFX", db.String, primary_key=True)
    start_date = db.Column("BLANKET_BEG_DATE", db.DateTime)
    end_date = db.Column("BLANKET_END_DATE", db.DateTime)
    dollar_limit = db.Column("BLANKET_DOLLAR_LIMIT", db.Float(precision=2))
    dollar_spent = db.Column("BLANKET_DOLLAR_TODATE", db.Float(precision=2))

    # column list for querying
    columns = (
        "contract_agency",
        "start_date",
        "end_date",
        "dollar_limit",
        "dollar_spent",
    )
