from fastapi import FastAPI
from routes import customer_routes, driver_routes, restaurant_routes
from utils.database import Base, engine

# Tạo bảng trong cơ sở dữ liệu
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Đăng ký routes
app.include_router(customer_routes.router, prefix="/api/customers", tags=["Customers"])
app.include_router(driver_routes.router, prefix="/api/drivers", tags=["Drivers"])
app.include_router(restaurant_routes.router, prefix="/api/restaurants", tags=["Restaurants"])
