from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

# Swim school
class Organisation(Base):
    __tablename__ = "organisations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    staff = relationship("Staff", back_populates="organisation")

# Staff members
class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    organisations = relationship("Organisation", secondary=organisation_staff, back_populates="staff_members")

# Qualification types
class Qualification(Base):
    __tablename__ = "qualifications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

# Staff qualifications
class StaffQualification(Base):
    __tablename__ = "staff_qualifications"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    qualification_id = Column(Integer, ForeignKey("qualifications.id"))
    expiry_date = Column(Date)
    active = Column(Boolean, default=True)

    staff = relationship("Staff", back_populates="qualifications")
    qualification = relationship("Qualification")

# class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    staff_members = relationship("Staff", secondary=organisation_staff, back_populates="organisations")

# -- ADDITIONS FOR QUALS --

import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Many-to-many association table
organisation_staff = Table(
    'organisation_staff',
    Base.metadata,
    Column('organisation_id', ForeignKey('organisations.id'), primary_key=True),
    Column('staff_id', ForeignKey('staff.id'), primary_key=True)
)

