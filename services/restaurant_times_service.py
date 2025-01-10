from sqlalchemy.orm import Session
from models import models, schemas
from models.schemas import DayEnum

# Lấy thông tin thời gian của một nhà hàng
def get_restaurant_times(restaurant_id: int, db: Session):
    return db.query(models.RestaurantTime).filter(models.RestaurantTime.restaurant_id == restaurant_id).all()

# Thêm thời gian cho nhà hàng
def create_restaurant_time(restaurant_id: int, time: schemas.RestaurantTimeCreate, db: Session):
    db_time = db.query(models.RestaurantTime).filter(
        models.RestaurantTime.restaurant_id == restaurant_id,
        models.RestaurantTime.day == time.day
    ).first()
    
    if db_time:
        return None  # Thời gian đã tồn tại
    
    new_time = models.RestaurantTime(
        restaurant_id=restaurant_id,
        day=time.day,
        open_time=time.open_time,
        close_time=time.close_time
    )
    db.add(new_time)
    db.commit()
    db.refresh(new_time)
    return new_time

# Cập nhật thời gian cho nhà hàng
def update_restaurant_time(restaurant_id: int, day: DayEnum, time: schemas.RestaurantTimeUpdate, db: Session):
    db_time = db.query(models.RestaurantTime).filter(
        models.RestaurantTime.restaurant_id == restaurant_id,
        models.RestaurantTime.day == day
    ).first()
    
    if not db_time:
        return None  # Thời gian không tồn tại
    
    db_time.open_time = time.open_time
    db_time.close_time = time.close_time
    db.commit()
    db.refresh(db_time)
    return db_time

# Xóa thời gian của nhà hàng
def delete_restaurant_time(restaurant_id: int, day: DayEnum, db: Session):
    db_time = db.query(models.RestaurantTime).filter(
        models.RestaurantTime.restaurant_id == restaurant_id,
        models.RestaurantTime.day == day
    ).first()
    
    if not db_time:
        return None  # Thời gian không tồn tại
    
    db.delete(db_time)
    db.commit()
    return db_time
