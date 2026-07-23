from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    reports = relationship("Report", back_populates="phone")

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    phone_id = Column(Integer, ForeignKey("phones.id"))

    report_text = Column(String)

    category = Column(String, default="Bilinmiyor")

    phone = relationship("Phone", back_populates="reports")

    