from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException
from typing import List


def create_customer(customer: schemas.CustomerCreate, db: Session):
    """
    Tạo Customer mới.
    """
    # Kiểm tra xem Customer đã tồn tại chưa
    db_customer = db.query(models.Customer).filter(models.Customer.name == customer.name).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Customer đã tồn tại")
    
    # Tạo và lưu Customer mới vào cơ sở dữ liệu
    new_customer = models.Customer(name=customer.name, is_deleted=customer.is_deleted)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)  # Refresh để lấy lại giá trị của customer_id
    return new_customer


def get_customer_by_id(customer_id: int, db: Session):
    """
    Lấy thông tin Customer theo ID.
    """
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer không tồn tại")
    return db_customer


def list_all_customers(db: Session) -> List[models.Customer]:
    """
    Lấy danh sách tất cả các Customers chưa bị xóa (is_deleted=False).
    """
    db_customers = db.query(models.Customer).filter(models.Customer.is_deleted == False).all()
    return db_customers


def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session):
    """
    Cập nhật thông tin của Customer.
    """
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer không tồn tại")
    
    # Cập nhật thông tin từ dữ liệu mới
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(customer_id: int, db: Session):
    """
    Đánh dấu xóa (is_deleted=True) thay vì xóa khỏi cơ sở dữ liệu.
    """
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer không tồn tại")
    
    # Đánh dấu Customer là đã xóa
    db_customer.is_deleted = True
    db.commit()
    return {"detail": "Customer đã bị xóa"}
