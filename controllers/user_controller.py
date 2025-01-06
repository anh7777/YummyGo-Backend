from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def register_user(db: Session, user_data):
    # Kiểm tra email đã tồn tại
    if db.query(User).filter(User.email == user_data['email']).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password và lưu người dùng mới
    hashed_password = get_password_hash(user_data['password'])
    new_user = User(
        user_name=user_data['user_name'],
        password=hashed_password,
        phone=user_data['phone'],
        email=user_data['email']
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
