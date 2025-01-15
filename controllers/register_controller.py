from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from services.register_service import *
from models.schemas import *
from models.models import *
from middlewares.auth_middleware import get_current_user

router = APIRouter(prefix="/register", tags=["Restaurants"])

# Đăng ký với vai trò khách hàng
@router.post("/customer")
async def register(user: UserCreate, customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        create_customer(user, customer, db)
        return {"message": "Đăng ký thành công với vai trò khách hàng."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi đăng ký khách hàng: {str(e)}")

# Đăng ký thêm vai trò khách hàng
@router.post("/add-customer")
async def add_role(customer: CustomerCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        become_customer(customer, current_user['user_id'], db)
        return {"message": "Thêm vai trò khách hàng thành công."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi thêm vai trò khách hàng: {str(e)}")

# Đăng ký với vai trò tài xế
@router.post("/driver")
async def register(user: UserCreate, driver: DriverCreate, db: Session = Depends(get_db)):
    try:
        create_driver(user, driver, db)
        return {"message": "Đăng ký thành công với vai trò tài xế."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi đăng ký tài xế: {str(e)}")

# Đăng ký thêm vai trò tài xế
@router.post("/add-driver")
async def add_role(driver: DriverCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        become_driver(driver, current_user['user_id'], db)
        return {"message": "Thêm vai trò tài xế thành công."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi thêm vai trò tài xế: {str(e)}")

# Đăng ký với vai trò nhà hàng
@router.post("/restaurant")
async def register(user: UserCreate, restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    try:
        create_restaurant(user, restaurant, db)
        return {"message": "Đăng ký thành công với vai trò nhà hàng."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi đăng ký nhà hàng: {str(e)}")

# Đăng ký thêm vai trò nhà hàng
@router.post("/add-restaurant")
async def add_role(restaurant: RestaurantCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        become_restaurant(restaurant, current_user['user_id'], db)
        return {"message": "Thêm vai trò nhà hàng thành công."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi khi thêm vai trò nhà hàng: {str(e)}")
