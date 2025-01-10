from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException

def create_order_item(order_item: schemas.OrderItemCreate, db: Session) -> models.OrderItem:
    db_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.item_id == order_item.item_id,
        models.OrderItem.order_id == order_item.order_id
    ).first()

    if db_order_item:
        raise HTTPException(status_code=400, detail="Mục đơn hàng đã tồn tại")

    new_order_item = models.OrderItem(
        item_id=order_item.item_id,
        order_id=order_item.order_id,
        price=order_item.price,
        quantity=order_item.quantity
    )
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    return new_order_item

def get_order_items(order_id: int, db: Session) -> list[models.OrderItem]:
    order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    if not order_items:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục đơn hàng")
    return order_items

def update_order_item(order_id: int, item_id: int, order_item: schemas.OrderItemCreate, db: Session) -> models.OrderItem:
    db_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id,
        models.OrderItem.item_id == item_id
    ).first()

    if not db_order_item:
        raise HTTPException(status_code=404, detail="Mục đơn hàng không tồn tại")

    db_order_item.price = order_item.price
    db_order_item.quantity = order_item.quantity
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def delete_order_item(order_id: int, item_id: int, db: Session) -> None:
    db_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id,
        models.OrderItem.item_id == item_id
    ).first()

    if not db_order_item:
        raise HTTPException(status_code=404, detail="Mục đơn hàng không tồn tại")

    db.delete(db_order_item)
    db.commit()
