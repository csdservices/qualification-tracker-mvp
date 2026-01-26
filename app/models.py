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
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    organisation = relationship("Organisation", back_populates="staff")
    qualifications = relationship("StaffQualification", back_populates="staff")

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
