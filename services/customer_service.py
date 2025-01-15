from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException, status
from typing import List
import random

def get_customer_by_id(customer_id: int, db: Session):
    """
    Lấy thông tin Customer theo ID.
    """
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer không tồn tại")
    return db_customer

def update_customer(customer_id: int, customer: CustomerCreate, db: Session):
    """
    Cập nhật thông tin của Customer.
    """
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer không tồn tại")
    
    # Cập nhật thông tin từ dữ liệu mới
    for key, value in customer.model_dump().items():
        if value is not None:
            if isinstance(value, str):
                if value == "":
                    continue
            setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(customer_id: int, db: Session):
    """
    Đánh dấu xóa (is_deleted=True) thay vì xóa khỏi cơ sở dữ liệu.
    """
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer không tồn tại")
    
    # Đánh dấu Customer là đã xóa
    db_customer.is_deleted = True
    db.commit()
    return {"detail": "Customer đã bị xóa"}

def create_order(order_id: int, customer_id: int, db: Session):
    db_order = db.query(Order).filter(Order.order_id == order_id,
                                      Order.customer_id == customer_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_drivers = db.query(Driver).filter(Driver.status == DriverStatusEnum.active,
                                         Driver.is_deleted == False).all()
    if not db_drivers:
        raise HTTPException(status_code=404, detail="Could not find active driver")
        
    driver = random.choice(db_drivers)

    db_order.driver_id = driver.driver_id
    db.commit()
    
    return db_order