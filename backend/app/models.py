from sqlalchemy import Column, Integer, String
from .database import Base


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)