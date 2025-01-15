from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.models import *
from models.schemas import *
from services.menu_item_service import (
    create_menu_item,
    list_menu_items,
    get_menu_item,
    update_menu_item_info,
    delete_menu_item,
    available_items
)
from middlewares.auth_middleware import get_current_user, require_role

router = APIRouter(prefix="/items", tags=["Menu Items"])

# Tạo menu_item mới, chỉ chủ nhà hàng có quyền này
# đầu vào là name, description, img_url, price 
@router.post("/create", response_model=MenuItemShchema)
async def add_item(menu_item: MenuItemCreate, current_restaurant: dict = Depends(require_role('restaurant')),db: Session = Depends(get_db)):
    return create_menu_item(menu_item, current_restaurant['user_id'], db)

# Lấy ra danh sách món ---> nhà hàng xem
@router.get("/all", response_model=List[MenuItemShchema])
async def get_all_menu_items(current_restaurant: dict = Depends(require_role('restaurant')),db: Session = Depends(get_db)):
    return list_menu_items(current_restaurant['user_id'], db)

# Lấy ra danh sách món available của nhà hàng ---> khách hàng duyệt món
@router.get("/available/{restaurant_id}", response_model=List[MenuItemShchema])
async def get_available_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    return available_items(restaurant_id, db)

# Lấy ra thông tin của một món dựa trên id
@router.get("/{item_id}", response_model=MenuItemShchema)
async def get_single_menu_item(item_id: int, db: Session = Depends(get_db)):
    return get_menu_item(item_id, db)

# Chỉnh sửa thông tin món
@router.put("/update/{item_id}", response_model=MenuItemShchema)
async def update_menu(item_id: int, menu_item: MenuItemUpdate, current_restaurant: dict = Depends(require_role("restaurant")), db: Session = Depends(get_db)):
    return update_menu_item_info(item_id, menu_item, current_restaurant["user_id"], db)

# Xóa món
@router.delete("/delete")
async def remove_menu_item(item_id: int, restaurant_id = Depends(require_role("restaurant")),db: Session = Depends(get_db)):
    return delete_menu_item(item_id, restaurant_id, db)

# Lấy ra danh sách món available của nhà hàng ---> khách hàng duyệt món
@router.get('/menu/{restaurant_id}', response_model=List[MenuItemShchema])
async def get_menu_by_res_id(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id,
                              MenuItem.is_deleted == False,
                              MenuItem.status == ItemStatusEnum.available).all()