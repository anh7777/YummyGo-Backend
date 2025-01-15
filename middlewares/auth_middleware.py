from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from typing import Annotated
from utils.access_token import decode_access_token
from typing import Annotated
# from fastapi.security import OAuth2PasswordBearer

# # OAuth2PasswordBearer để lấy token từ header
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Middleware để xác thực JWT và phân quyền
async def get_current_user(request: Request):
    try:
        # Giải mã token và lấy user_id
        token = request.cookies.get("access_token")    
        user_info = decode_access_token(token)
        user_id = user_info["user_id"]
        role = user_info["role"]  
        return {"user_id": user_id, "role": role}
    except HTTPException as e:
        raise e


# Hàm kiểm tra quyền truy cập dựa trên vai trò
def require_role(required_role: str):
    def wrapper(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
        return current_user
    return wrapper