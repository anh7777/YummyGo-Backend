from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException
from typing import List

# ------------------------------
# Quản lý Logic Nghiệp Vụ Tài Xế
# ------------------------------

def get_driver_service(driver_id: int, db: Session):
    """Lấy thông tin tài xế theo ID"""
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    return driver


def update_driver_service(driver: DriverUpdate, driver_id: int, db: Session):
    """Cập nhật thông tin tài xế"""
    db_driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    
    
    for key, value in driver.model_dump().items():
        if value is not None:
            if isinstance(value, str):
                if value == "":
                    continue
            setattr(db_driver, key, value)        
    db.commit()
    db.refresh(db_driver)
    return db_driver


# Cập nhật trạng thái tài xế
def update_driver_status(driver_id: int, db: Session):
    db_driver = db.query(Driver).filter(Driver.driver_id == driver_id, Driver.is_deleted == False)
    driver = db_driver.first()
    if not driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    if driver.status == DriverStatusEnum.active:
        db_driver.update({Driver.status: DriverStatusEnum.inactive})
    elif driver.status == DriverStatusEnum.inactive:
        db_driver.update({Driver.status: DriverStatusEnum.active})

    db.commit()
    return driver


def delete_driver_service(driver_id: int, db: Session):
    """Xóa tài xế (đánh dấu is_deleted là True)"""
    db_driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    
    db_driver.is_deleted = True
    db.commit()
    db.refresh(db_driver)
    return db_driver


def get_current_driver_order(driver_id: int, db: Session):
    db_order = db.query(Order).filter(Order.driver_id == driver_id,
                                      Order.order_status == OrderStatusEnum.cart).first()
    if not db_order:
        return []
    return db_order.order_id

def get_driver_orders(driver_id: int, db: Session):
    db_order = db.query(Order).filter(Order.driver_id == driver_id).all()
    if not db_order:
        return []
    return db_order
# def list_drivers_service(db: Session) -> List[Driver]:
#     """Lấy danh sách tất cả tài xế chưa bị xóa"""
#     return db.query(Driver).filter(Driver.is_deleted == False).all()

