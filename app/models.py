import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime
)
from sqlalchemy.orm import relationship

from .database import Base


# ---------- Association Table ----------
organisation_staff = Table(
    "organisation_staff",
    Base.metadata,
    Column("organisation_id", ForeignKey("organisations.id"), primary_key=True),
    Column("staff_id", ForeignKey("staff.id"), primary_key=True),
)


# ---------- Models ----------
class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    staff_members = relationship(
        "Staff",
        secondary=organisation_staff,
        back_populates="organisations"
    )


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    organisations = relationship(
        "Organisation",
        secondary=organisation_staff,
        back_populates="staff_members"
    )

