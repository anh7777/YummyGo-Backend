from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services import merchant_service
from db.database import get_db
from models import schemas

router = APIRouter(prefix="/merchants", tags=["Merchants"])

# Create merchant
@router.post("/", response_model=schemas.Merchant)
async def create_merchant(merchant: schemas.MerchantCreate, db: Session = Depends(get_db)):
    new_merchant = merchant_service.create_merchant(merchant, db)
    if not new_merchant:
        raise HTTPException(status_code=400, detail="Merchant đã tồn tại")
    return new_merchant

# Get merchant by id
@router.get("/{merchant_id}", response_model=schemas.Merchant)
async def get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    merchant = merchant_service.get_merchant(merchant_id, db)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant không tồn tại")
    return merchant

# Get all merchants
@router.get("/", response_model=List[schemas.Merchant])
async def list_merchants(db: Session = Depends(get_db)):
    return merchant_service.list_merchants(db)

# Delete merchant
@router.delete("/{merchant_id}")
async def delete_merchant(merchant_id: int, db: Session = Depends(get_db)):
    merchant = merchant_service.delete_merchant(merchant_id, db)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant không tồn tại")
    return {"detail": "Merchant đã bị xóa"}
