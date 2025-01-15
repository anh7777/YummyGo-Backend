from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException


def get_order_items(order_id: int, db: Session) -> list[OrderItem]:
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    if not order_items:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục đơn hàng")
    return order_items

def delete_order_item(order_id: int, item_id: int, db: Session) -> None:
    db_order_item = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.item_id == item_id
    ).first()

    if not db_order_item:
        raise HTTPException(status_code=404, detail="Mục đơn hàng không tồn tại")

    db.delete(db_order_item)
    db.commit()
