from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import schemas
from models.schemas import DayEnum
from db.database import get_db
from services import restaurant_times_service as services

router = APIRouter(prefix="/restaurant_times", tags=["Restaurant Times"])

# ------------------------------
# Quản lý Thời gian Nhà Hàng
# ------------------------------

# Lấy thông tin thời gian của một nhà hàng
@router.get("/{restaurant_id}/times", response_model=List[schemas.RestaurantTimeResponse])
async def get_restaurant_times(restaurant_id: int, db: Session = Depends(get_db)):
    times = services.get_restaurant_times(restaurant_id, db)
    if not times:
        raise HTTPException(status_code=404, detail="Không tìm thấy thời gian nhà hàng")
    return times

# Thêm thời gian cho nhà hàng
@router.post("/{restaurant_id}/times", response_model=schemas.RestaurantTimeResponse)
async def create_restaurant_time(restaurant_id: int, time: schemas.RestaurantTimeCreate, db: Session = Depends(get_db)):
    new_time = services.create_restaurant_time(restaurant_id, time, db)
    
    if not new_time:
        raise HTTPException(status_code=400, detail="Thời gian cho ngày này đã tồn tại")
    
    return new_time

# Cập nhật thời gian cho nhà hàng
@router.put("/{restaurant_id}/times/{day}", response_model=schemas.RestaurantTimeResponse)
async def update_restaurant_time(restaurant_id: int, day: DayEnum, time: schemas.RestaurantTimeUpdate, db: Session = Depends(get_db)):
    updated_time = services.update_restaurant_time(restaurant_id, day, time, db)
    
    if not updated_time:
        raise HTTPException(status_code=404, detail="Thời gian không tồn tại")
    
    return updated_time

# Xóa thời gian của nhà hàng
@router.delete("/{restaurant_id}/times/{day}")
async def delete_restaurant_time(restaurant_id: int, day: DayEnum, db: Session = Depends(get_db)):
    deleted_time = services.delete_restaurant_time(restaurant_id, day, db)
    
    if not deleted_time:
        raise HTTPException(status_code=404, detail="Thời gian không tồn tại")
    
    return {"detail": f"Thời gian cho {day} đã bị xóa"}
