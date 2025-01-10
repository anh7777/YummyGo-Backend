from sqlalchemy.orm import Session
from models import models
from models import schemas

def create_user_service(user: schemas.UserCreate, db: Session) -> models.User:
    db_user = db.query(models.User).filter(models.User.user_name == user.user_name).first()
    if db_user:
        raise Exception("Username already exists")
    
    # Hash the password before saving (add actual hashing logic here)
    hashed_password = user.password

    db_user = models.User(
        user_name=user.user_name,
        password=hashed_password,
        phone=user.phone,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_service(user_id: int, db: Session) -> models.User:
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise Exception("User not found")
    return db_user

def list_users_service(db: Session) -> list:
    return db.query(models.User).filter(models.User.is_deleted == False).all()

def update_user_service(user_id: int, user: schemas.UserUpdate, db: Session) -> models.User:
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise Exception("User not found")
    
    if user.user_name:
        db_user.user_name = user.user_name
    if user.password:
        db_user.password = user.password
    if user.phone:
        db_user.phone = user.phone
    if user.email:
        db_user.email = user.email
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_service(user_id: int, db: Session) -> str:
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise Exception("User not found")
    
    db_user.is_deleted = True
    db.commit()
    return "Xóa người dùng thành công"
