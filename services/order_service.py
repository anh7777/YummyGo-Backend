from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.models import Order as OrderModel
from models.schemas import OrderCreate, OrderUpdate
from datetime import datetime

def create_order(order: OrderCreate, db: Session):
    db_order = OrderModel(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(OrderModel).all()

def get_order(order_id: int, db: Session):
    db_order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

def update_order(order_id: int, order_update: OrderUpdate, db: Session):
    db_order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Cập nhật trạng thái
    db_order.order_status = order_update.order_status
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(order_id: int, db: Session):
    db_order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return {"detail": "Đơn hàng đã bị xóa."}
