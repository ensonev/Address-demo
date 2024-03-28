from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import Address, AddressOut, AddressData
from db import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/addresses/", response_model=List[AddressOut])
def get_addresses(db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    return addresses

@app.get("/addresses/{address_id}", response_model=AddressOut)
def get_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.post("/addresses/", response_model=AddressOut)
def add_address(address: AddressData, db: Session = Depends(get_db)):
    current_datetime = datetime.now()
    db_address = Address(**address.dict(), created_at=current_datetime, updated_at=current_datetime)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.put("/addresses/{address_id}", response_model=AddressOut)
def put_address(address_id: int, address: AddressData, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db_address.updated_at = datetime.now()
    db.commit()
    db.refresh(db_address)
    return db_address

@app.patch("/addresses/{address_id}", response_model=AddressOut)
def patch_address(address_id: int, address: AddressData, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict(exclude_unset=True).items():
        setattr(db_address, key, value)
    db_address.updated_at = datetime.now()
    db.commit()
    db.refresh(db_address)
    return db_address

@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return HTTPException(status_code=204, detail="Address deleted successfully")
