from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from fastapi import HTTPException
from utils.security import hash_password


# Đăng ký thêm vai trò khách hàng
def become_customer(customer: CustomerCreate, user_id: int, db: Session):
    db_customer = db.query(Customer).filter(Customer.customer_id == user_id).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Customer already exists")
    new_customer = Customer(
        customer_id = user_id,
        name=customer.name
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Đăng ký vai trò khách hàng
def create_customer(user: UserCreate, customer: CustomerCreate, db: Session):
    db_user = db.query(User).filter(User.user_name == user.user_name).first()
    if db_user:
        raise Exception("User already exists")
    
    # Hash the password before saving (add actual hashing logic here)
    hashed_password = hash_password(user.password).decode()

    db_user = User(
        user_name=user.user_name,
        password=hashed_password,
        phone=user.phone,
        email=user.email
    )
    db.add(db_user)
    db.commit()  
    db.refresh(db_user)  
    user_id = db_user.user_id
    
    try:        
        db_customer = Customer(
            customer_id=user_id,
            name=customer.name
        )
    except Exception as e:
        db.delete(db_user)
        db.commit()
        raise e
       
    db.add(db_customer)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_customer)
    return db_user


# Đăng ký thêm vai trò tài xế
def become_driver(driver: DriverCreate, user_id: int, db: Session):
    db_driver = db.query(Driver).filter(Driver.driver_id == user_id).first()
    if db_driver:
        raise HTTPException(status_code=400, detail="Driver already exists")
    new_driver = Driver(
        driver_id = user_id,
        name=driver.name
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

# Đăng ký vai trò tài xế
def create_driver(user: UserCreate, driver: DriverCreate, db: Session):
    db_user = db.query(User).filter(User.user_name == user.user_name).first()
    if db_user:
        raise Exception("User already exists")
    
    # Hash the password before saving (add actual hashing logic here)
    hashed_password = hash_password(user.password).decode()

    db_user = User(
        user_name=user.user_name,
        password=hashed_password,
        phone=user.phone,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  
    user_id = db_user.user_id
    try:        
        db_driver = Driver(
            driver_id=user_id,
            name=driver.name
        )
    except Exception as e:
        db.delete(db_user)
        db.commit()
        raise e
    
    db.add(db_driver)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_driver)
    return db_user


# Đăng ký thêm vai trò nhà hàng
def become_restaurant(restaurant: RestaurantCreate, user_id: int, db: Session):
    db_restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == user_id).first()
    if db_restaurant:
        raise HTTPException(status_code=400, detail="Nhà hàng đã tồn tại")
    new_restaurant = Restaurant(
        restaurant_id = user_id,
        name=restaurant.name,
        category=restaurant.category,
        address=restaurant.address,
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

# Đăng ký vai trò nhà hàng
def create_restaurant(user: UserCreate, restaurant: RestaurantCreate, db: Session):
    db_user = db.query(User).filter(User.user_name == user.user_name).first()
    if db_user:
        raise Exception("Username already exists")
    
    # Hash the password before saving (add actual hashing logic here)
    hashed_password = hash_password(user.password).decode()

    db_user = User(
        user_name=user.user_name,
        password=hashed_password,
        phone=user.phone,
        email=user.email
    )
    
    db.add(db_user)
    db.refresh(db_user)  
    db.commit()
    user_id = db_user.user_id
    
    try:
        db_restaurant = Restaurant(
            restaurant_id=user_id,
            name=restaurant.name,
            category=restaurant.category,
            address=restaurant.address
        )
        db.add(db_restaurant)
    except Exception as e:
        db.delete(db_user)
        db.commit()
        raise e
    db.commit()
    db.refresh(db_user)
    db.refresh(db_restaurant)
    return True