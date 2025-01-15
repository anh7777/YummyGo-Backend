from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException, status
from utils.security import verify_password

def authenticate_login(user: UserLogin, db: Session):
    user_info = db.query(User).filter(User.user_name == user.user_name, 
                                      User.is_deleted == False).first()
    password_verified = verify_password(user.password, user_info.password)
    
    if not user_info or not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu sai",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = user_info.user_id
    role = None
    if user.role == RoleEnum.customer:
        customer = db.query(Customer).filter(Customer.customer_id == user_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bạn chưa có tài khoản khách hàng",
                headers={"WWW-Authenticate": "Bearer"},                
            )
        role = "customer"
        
    elif user.role == RoleEnum.driver:
        driver = db.query(Driver).filter(Driver.driver_id == user_id).first()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bạn chưa có tài khoản tài xế",
                headers={"WWW-Authenticate": "Bearer"},                
            )
        role = "driver"
    elif user.role == RoleEnum.restaurant:
        restaurant_id = db.query(Restaurant).filter(Restaurant.restaurant_id == user_id).first()
        if not restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bạn chưa có tài khoản nhà hàng",
                headers={"WWW-Authenticate": "Bearer"},                
            )
        role = "restaurant"
    return user_id, role