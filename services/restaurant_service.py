from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException
from models import models

# Lấy thông tin nhà hàng theo ID ---> khách xem
def get_restaurant(restaurant_id: int, db: Session):
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id,
                                             Restaurant.is_deleted == False,
                                             Restaurant.status == RestaurantStatusEnum.active).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    return restaurant

# Lấy thông tin nhà hàng theo ID ---> nhà hàng xem
def get_restaurant_info(restaurant_id: int, db: Session):
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id,
                                             Restaurant.is_deleted == False).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    return restaurant

# Lấy danh sách nhà hàng để khách hàng duyệt
def list_restaurants(db: Session):
    return db.query(Restaurant).filter(Restaurant.is_deleted == False,
                                       Restaurant.status == RestaurantStatusEnum.active).all()

# Cập nhật thông tin nhà hàng
def update_restaurant(restaurant: RestaurantUpdate, restaurant_id: int, db: Session):
    db_restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id, Restaurant.is_deleted == False).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    for key, value in restaurant.model_dump(exclude_unset=True).items():
        if value is not None:
            if isinstance(value, str):
                if value == "":
                    continue
            setattr(db_restaurant, key, value)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

# Cập nhật trạng thái nhà hàng
def update_restaurant_status(restaurant_id: int, db: Session):
    db_restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id,
                                                Restaurant.is_deleted == False)
    restaurant = db_restaurant.first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    if restaurant.status == RestaurantStatusEnum.active:
        db_restaurant.update({Restaurant.status: RestaurantStatusEnum.inactive})
    elif restaurant.status == RestaurantStatusEnum.inactive:
        db_restaurant.update({Restaurant.status: RestaurantStatusEnum.active})

    db.commit()
    return restaurant

# Xóa nhà hàng
def delete_restaurant(restaurant_id: int, db: Session):
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    restaurant.is_deleted = True
    db.commit()
    return {"detail": "Nhà hàng đã bị xóa"}

# Lấy ra danh sách đơn hàng hiện tại của nhà hàng
def get_current_restaurant_order(restaurant_id: int, db: Session):
    db_order = db.query(Order).filter(Order.restaurant_id == restaurant_id,
                                      Order.order_status == OrderStatusEnum.preparing).all()
    if not db_order:
        return None
    return [order.order_id for order in db_order]
