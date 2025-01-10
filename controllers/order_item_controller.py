from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from services import order_item_service
from models import schemas

router = APIRouter(prefix="/oder_items", tags=["Oder Items"])

# ------------------------------
# Quản lý Order Items
# ------------------------------

@router.post("/", response_model=schemas.OrderItem)
async def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return order_item_service.create_order_item(order_item, db)

@router.get("/{order_id}", response_model=List[schemas.OrderItem])
async def get_order_items(order_id: int, db: Session = Depends(get_db)):
    return order_item_service.get_order_items(order_id, db)

@router.put("/{order_id}/{item_id}", response_model=schemas.OrderItem)
async def update_order_item(order_id: int, item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return order_item_service.update_order_item(order_id, item_id, order_item, db)

@router.delete("/{order_id}/{item_id}")
async def delete_order_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
    order_item_service.delete_order_item(order_id, item_id, db)
    return {"detail": "Mục đơn hàng đã bị xóa"}
