from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException

# Tạo nhà hàng mới
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant.name).first()
    if db_restaurant:
        raise HTTPException(status_code=400, detail="Nhà hàng đã tồn tại")
    new_restaurant = models.Restaurant(
        name=restaurant.name,
        category=restaurant.category,
        phone=restaurant.phone,
        address=restaurant.address,
        coord=restaurant.coord,
        status=restaurant.status
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

# Lấy thông tin nhà hàng theo ID
def get_restaurant(restaurant_id: int, db: Session):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    return restaurant

# Lấy danh sách nhà hàng
def list_restaurants(db: Session):
    return db.query(models.Restaurant).filter(models.Restaurant.is_deleted == False).all()

# Cập nhật nhà hàng
def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: Session):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    for key, value in restaurant.dict(exclude_unset=True).items():
        setattr(db_restaurant, key, value)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

# Xóa nhà hàng
def delete_restaurant(restaurant_id: int, db: Session):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    restaurant.is_deleted = True
    db.commit()
    return {"detail": "Nhà hàng đã bị xóa"}