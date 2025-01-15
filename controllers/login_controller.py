from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.schemas import *
from fastapi.responses import JSONResponse
from services.login_service import authenticate_login
from utils.access_token import create_access_token
from datetime import timedelta
from services.connection_manager import ConnectionManager

router = APIRouter()

# endpoint đăng nhập
@router.post("/token")
async def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    user_id, role = authenticate_login(user, db)
    if not user_id:
        raise HTTPException(status_code=401, detail="Thông tin đăng nhập không hợp lệ")
    access_token = create_access_token({"user_id": user_id, "role": role})
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        path="/",
        httponly=True,
        secure=False,  
        max_age=timedelta(days=3),
        expires=timedelta(days=3),
        samesite="Strict" 
    )
    ConnectionManager.add_user(user_id)
    
    return {"message": "Đăng nhập thành công"}

