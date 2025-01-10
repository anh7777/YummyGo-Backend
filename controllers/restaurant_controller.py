from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from services import restaurant_service
from models import schemas

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# Tạo nhà hàng mới
@router.post("/", response_model=schemas.Restaurant)
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return restaurant_service.create_restaurant(restaurant, db)

# Lấy thông tin nhà hàng theo ID
@router.get("/{restaurant_id}", response_model=schemas.Restaurant)
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_service.get_restaurant(restaurant_id, db)

# Lấy danh sách nhà hàng
@router.get("/", response_model=List[schemas.Restaurant])
async def list_restaurants(db: Session = Depends(get_db)):
    return restaurant_service.list_restaurants(db)

# Cập nhật nhà hàng
@router.put("/{restaurant_id}", response_model=schemas.Restaurant)
async def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: Session = Depends(get_db)):
    return restaurant_service.update_restaurant(restaurant_id, restaurant, db)

# Xóa nhà hàng
@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_service.delete_restaurant(restaurant_id, db)
