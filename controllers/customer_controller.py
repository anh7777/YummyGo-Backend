from fastapi import Request, Response, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.schemas import *
from models.models import *
from db.database import get_db
from middlewares.auth_middleware import get_current_user, require_role
from services.customer_service import (
    get_customer_by_id,
    create_order,
    update_customer,
    delete_customer,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


# Lấy thông tin customer
# api này sẽ dùng để hiện thông tin của customer cùng
# với /user/me
@router.get("/me", response_model=CustomerSchema)
async def get_customer(current_customer: dict = Depends(require_role('customer')), db: Session = Depends(get_db)):
    return get_customer_by_id(current_customer['user_id'], db)

# Sửa thông tin customer
# sử dụng kết hợp với /user/update
@router.put("/update", response_model=CustomerSchema)
async def update_existing_customer(customer: CustomerCreate, current_customer: dict = Depends(require_role('customer')), db: Session = Depends(get_db)):
    return update_customer(current_customer, customer, db)

# Xóa customer ---> is_deleted = True
@router.delete("/delete")
async def delete_existing_customer(current_customer: dict = Depends(require_role('customer')), db: Session = Depends(get_db)):
    return delete_customer(current_customer, db)

# @router.get("/", response_model=List[CustomerSchema])
# async def list_customers(db: Session = Depends(get_db)):
#     return list_all_customers(db)

@router.put("/send-order/{order_id}")
async def create_an_order(order_id: int, current_customer: dict = Depends(require_role('customer')), db: Session = Depends(get_db)):
    return create_order(order_id, current_customer['user_id'], db)
