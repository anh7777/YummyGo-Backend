from sqlalchemy.orm import Session
from models import models, schemas

def create_merchant(merchant: schemas.MerchantCreate, db: Session):
    db_merchant = db.query(models.Merchant).filter(models.Merchant.name == merchant.name).first()
    if db_merchant:
        return None  # Merchant already exists
    new_merchant = models.Merchant(name=merchant.name)
    db.add(new_merchant)
    db.commit()
    db.refresh(new_merchant)
    return new_merchant

def get_merchant(merchant_id: int, db: Session):
    return db.query(models.Merchant).filter(models.Merchant.merchant_id == merchant_id).first()

def list_merchants(db: Session):
    return db.query(models.Merchant).filter(models.Merchant.is_deleted == False).all()

def delete_merchant(merchant_id: int, db: Session):
    merchant = db.query(models.Merchant).filter(models.Merchant.merchant_id == merchant_id).first()
    if not merchant:
        return None  # Merchant does not exist
    merchant.is_deleted = True
    db.commit()
    return merchant
