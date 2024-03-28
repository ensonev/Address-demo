from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


Base = declarative_base()

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)
    postal_code = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str

class AddressData(AddressBase):
    pass

class AddressOut(BaseModel):
    id: int
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
