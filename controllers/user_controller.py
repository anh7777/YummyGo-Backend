from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.schemas import *
from models.models import *
from services.user_service import *
from fastapi.responses import JSONResponse
from middlewares.auth_middleware import *
 
router = APIRouter(prefix="/users", tags=["Users"])

# lấy thông tin user bao gồm: user_name, phone, email
@router.get("/me")
async def get_user_(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_user = get_user(current_user['user_id'], db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))    

# Cập nhật thông tin tài khoản, api đã được thiết kế để dù truyền vào bao nhiêu tham số
# cũng update được, có thể sử dụng linh hoạt cho từng thông tin được chỉnh sửa
# nếu gửi json rỗng hoặc chuỗi rỗng thì sẽ không update
@router.put("/update")
async def update_user_info(user: UserUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user(user, current_user['user_id'], db)

# @router.get("/", response_model=List[User])
# async def list_users(db: Session = Depends(get_db)):
#     return list_users(db)

# xóa user
@router.delete("/delete")
async def delete_user_(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        message = delete_user(current_user['user_id'], db)
        return {"detail": message}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
