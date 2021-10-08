# pylint: disable=W0611
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
)

Base = declarative_base()


def init_po_joint_key(
    po_col: str = "PO_NBR", release_col: str = "RELEASE_NBR"
) -> ForeignKeyConstraint:
    """Creates a ForeignKeyConstraint for po_number and release_number

    Parameters
    ----------
    po_col: str
        The name of the column on the src table that references po_number
    release_col: str
        The name of the column on the src table that references release_number

    Returns
    -------
    ForeignKeyConstraint
        Returns a ForeignKeyConstraint for the table for po and release number
    """
    joint_key = ForeignKeyConstraint(
        [po_col, release_col],
        ["PO_HEADER.PO_NBR", "PO_HEADER.RELEASE_NBR"],
    )
    return joint_key
