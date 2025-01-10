from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services import order_service
from models.schemas import Order, OrderCreate, OrderUpdate
from db.database import get_db

router = APIRouter(prefix="/oders", tags=["Oders"])

# Tạo đơn hàng mới
@router.post("/", response_model=Order)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(order, db)

# Lấy danh sách đơn hàng
@router.get("/", response_model=List[Order])
async def get_orders(db: Session = Depends(get_db)):
    return order_service.get_orders(db)

# Lấy đơn hàng theo ID
@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(order_id, db)

# Cập nhật trạng thái đơn hàng
@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    return order_service.update_order(order_id, order_update, db)

# Xóa đơn hàng
@router.delete("/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.delete_order(order_id, db)
