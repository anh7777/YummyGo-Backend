from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from services.restaurant_service import *
from models.schemas import *
from models.models import *
from middlewares.auth_middleware import get_current_user, require_role

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
    
#Lấy thông tin nhà hàng --> cho tài khoản nhà hàng xem
@router.get("/me")
async def get_restaurant_me(current_restaurant: dict = Depends(require_role('restaurant')), db: Session = Depends(get_db)):
    return get_restaurant_info(current_restaurant['user_id'], db)

# Cập nhật thông tin nhà hàng
@router.put("/update")
async def update_restaurant_(restaurant: RestaurantUpdate, current_restaurant: dict = Depends(require_role('restaurant')), db: Session = Depends(get_db)):
    return update_restaurant(restaurant, current_restaurant['user_id'], db)

# Xóa nhà hàng
@router.delete("/delete")
async def delete_restaurant_(current_restaurant: dict = Depends(require_role('restaurant')), db: Session = Depends(get_db)):
    return delete_restaurant(current_restaurant['user_id'], db)

#Chuyển trạng thái hoạt động của nhà hàng
@router.put("/change-status")
async def change_status(current_restaurant: dict = Depends(require_role('restaurant')), db: Session = Depends(get_db)):
    restaurant = update_restaurant_status(current_restaurant['user_id'], db)
    return {"message" : "status changed", "status": restaurant.status}

# Lấy ra danh sách mã đơn hàng hiện tại của nhà hàng
# Dùng mã đơn để hiển thị các món trong đơn hàng khi nhà hàng
# chọn xem đơn
@router.get("/orders")
async def restaurant_orders(current_restaurant: dict = Depends(require_role('restaurant')), db: Session = Depends(get_db)):
    return get_current_restaurant_order(current_restaurant['user_id'], db)

# Lấy danh sách các nhà hàng đang active --> customer duyệt
@router.get("/active")
async def list_restaurants_(db: Session = Depends(get_db)):
    return list_restaurants(db)

# Lấy thông tin nhà hàng theo ID ---> hiện trên giao diện customer
@router.get("/{restaurant_id}", response_model=RestaurantSchema)
async def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    return get_restaurant(restaurant_id, db)
