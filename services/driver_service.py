from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException
from typing import List

# ------------------------------
# Quản lý Logic Nghiệp Vụ Tài Xế
# ------------------------------

def create_driver_service(driver: schemas.DriverCreate, db: Session):
    """Tạo tài xế mới"""
    db_driver = db.query(models.Driver).filter(models.Driver.name == driver.name).first()
    if db_driver:
        raise HTTPException(status_code=400, detail="Tài xế đã tồn tại")
    
    new_driver = models.Driver(name=driver.name, status=driver.status)
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


def list_drivers_service(db: Session) -> List[schemas.Driver]:
    """Lấy danh sách tất cả tài xế chưa bị xóa"""
    return db.query(models.Driver).filter(models.Driver.is_deleted == False).all()


def get_driver_service(driver_id: int, db: Session):
    """Lấy thông tin tài xế theo ID"""
    driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    return driver


def update_driver_service(driver_id: int, driver: schemas.DriverCreate, db: Session):
    """Cập nhật thông tin tài xế"""
    db_driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    
    db_driver.name = driver.name
    db_driver.status = driver.status
    db.commit()
    db.refresh(db_driver)
    return db_driver


def delete_driver_service(driver_id: int, db: Session):
    """Xóa tài xế (đánh dấu is_deleted là True)"""
    db_driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Tài xế không tồn tại")
    
    db_driver.is_deleted = True
    db.commit()
    db.refresh(db_driver)
    return db_driver
