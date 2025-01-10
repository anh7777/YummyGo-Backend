from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import schemas
from db.database import get_db
from services.customer_service import (
    create_customer,
    get_customer_by_id,
    list_all_customers,
    update_customer,
    delete_customer,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=schemas.Customer)
async def create_new_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(customer, db)


@router.get("/{customer_id}", response_model=schemas.Customer)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_by_id(customer_id, db)


@router.get("/", response_model=List[schemas.Customer])
async def list_customers(db: Session = Depends(get_db)):
    return list_all_customers(db)


@router.put("/{customer_id}", response_model=schemas.Customer)
async def update_existing_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return update_customer(customer_id, customer, db)


@router.delete("/{customer_id}")
async def delete_existing_customer(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(customer_id, db)
