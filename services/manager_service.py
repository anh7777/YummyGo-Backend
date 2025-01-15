from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException

def create_manager_service(manager: ManagerCreate, db: Session):
    """Tạo mới một Manager."""
    # Kiểm tra nếu username đã tồn tại
    db_manager = db.query(Manager).filter(Manager.username == manager.username).first()
    if db_manager:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    
    # Tạo manager mới
    new_manager = Manager(
        username=manager.username,
        password=manager.password,  # Mã hóa mật khẩu nếu cần
        name=manager.name,
        restaurant_id=manager.restaurant_id
    )
    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)
    return new_manager


def get_manager_service(manager_id: int, db: Session):
    """Lấy thông tin Manager dựa trên ID."""
    db_manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not db_manager:
        raise HTTPException(status_code=404, detail="Manager không tồn tại")
    return db_manager


def update_manager_service(manager_id: int, manager: ManagerCreate, db: Session):
    """Cập nhật thông tin của Manager."""
    db_manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not db_manager:
        raise HTTPException(status_code=404, detail="Manager không tồn tại")
    
    # Cập nhật thông tin manager
    db_manager.username = manager.username
    db_manager.password = manager.password  # Mã hóa mật khẩu nếu cần
    db_manager.name = manager.name
    db_manager.restaurant_id = manager.restaurant_id
    
    db.commit()
    db.refresh(db_manager)
    return db_manager


def delete_manager_service(manager_id: int, db: Session):
    """Xóa Manager dựa trên ID."""
    db_manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not db_manager:
        raise HTTPException(status_code=404, detail="Manager không tồn tại")
    
    db.delete(db_manager)
    db.commit()
    return {"detail": "Manager đã bị xóa"}
