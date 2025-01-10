from sqlalchemy.orm import Session
from typing import List
from models import models, schemas
from fastapi import HTTPException


def create_menu_item(menu_item: schemas.MenuItemCreate, db: Session) -> models.MenuItem:
    """
    Tạo một menu item mới.
    """
    # Kiểm tra nếu nhà hàng có trong cơ sở dữ liệu
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == menu_item.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")

    # Tạo mới menu item
    new_menu_item = models.MenuItem(**menu_item.dict())
    db.add(new_menu_item)
    db.commit()
    db.refresh(new_menu_item)
    return new_menu_item


def list_menu_items(db: Session) -> List[models.MenuItem]:
    """
    Lấy danh sách tất cả menu items chưa bị xóa.
    """
    return db.query(models.MenuItem).filter(models.MenuItem.is_deleted == False).all()


def get_menu_item(item_id: int, db: Session) -> models.MenuItem:
    """
    Lấy thông tin chi tiết của một menu item theo ID.
    """
    menu_item = db.query(models.MenuItem).filter(models.MenuItem.item_id == item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Món ăn không tồn tại")
    return menu_item


def update_menu_item(item_id: int, menu_item: schemas.MenuItemUpdate, db: Session) -> models.MenuItem:
    """
    Cập nhật thông tin của một menu item.
    """
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.item_id == item_id).first()
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Món ăn không tồn tại")
    
    # Cập nhật thông tin
    for key, value in menu_item.dict(exclude_unset=True).items():
        setattr(db_menu_item, key, value)

    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def delete_menu_item(item_id: int, db: Session):
    """
    Xóa mềm (soft delete) một menu item.
    """
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.item_id == item_id).first()
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Món ăn không tồn tại")
    
    # Soft delete bằng cách cập nhật `is_deleted` thành True
    db_menu_item.is_deleted = True
    db.commit()
    return {"detail": "Món ăn đã bị xóa"}
