from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from decimal import Decimal
from datetime import datetime, time


# ------------------------------
# Mô hình User (Người dùng)
# ------------------------------

class UserBase(BaseModel):
    user_name: str  # Tên người dùng
    phone: Optional[str] = None  # Số điện thoại, có thể rỗng
    email: Optional[EmailStr] = None  # Email, có thể rỗng

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class UserCreate(UserBase):
    password: str  # Mật khẩu khi tạo người dùng mới

class User(UserBase):
    user_id: int  # ID người dùng
    is_deleted: bool  # Trạng thái xóa người dùng (True nếu đã xóa)

class UserUpdate(UserBase):
    password: Optional[str] = None  # Mật khẩu có thể thay đổi khi cập nhật
    phone: Optional[str] = None  # Số điện thoại có thể thay đổi
    email: Optional[EmailStr] = None  # Email có thể thay đổi


# ------------------------------
# Mô hình Merchant (Nhà cung cấp)
# ------------------------------

class MerchantBase(BaseModel):
    name: str  # Tên nhà cung cấp

class MerchantCreate(MerchantBase):
    pass  # Khi tạo mới, không cần thêm thuộc tính gì ngoài tên

class Merchant(MerchantBase):
    merchant_id: int  # ID nhà cung cấp
    is_deleted: bool = False  # Trạng thái xóa nhà cung cấp, mặc định là False

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class MerchantUpdate(MerchantBase):
    name: Optional[str] = None  # Tên nhà cung cấp có thể thay đổi


# ------------------------------
# Mô hình Restaurant (Nhà hàng)
# ------------------------------

class CategoryEnum(str, Enum):
    bun_pho_chao = "Bún - Phở - Cháo"
    banh_mi_xoi = "Bánh Mì - Xôi"
    ga_ran_burger = "Gà rán - Burger"
    com = "Cơm"
    hai_san = "Hải sản"
    do_chay = "Đồ chay"
    ca_phe = "Cà phê"
    tra_sua = "Trà sữa"
    trang_mieng = "Tráng miệng"
    an_vat = "Ăn vặt"
    pizza_my_y = "Pizza - Mì Ý"
    banh_viet_nam = "Bánh Việt Nam"
    lau_nuong = "Lẩu - Nướng"

class RestaurantStatusEnum(str, Enum):
    active = "active"  # Nhà hàng hoạt động
    inactive = "inactive"  # Nhà hàng không hoạt động
    # closed = "closed"  # Nhà hàng đã đóng cửa

class RestaurantBase(BaseModel):
    name: str  # Tên nhà hàng
    category: CategoryEnum  # Loại nhà hàng
    phone: Optional[str] = None  # Số điện thoại, có thể rỗng
    address: str  # Địa chỉ nhà hàng
    coord: str  # Tọa độ nhà hàng, có thể thay bằng kiểu POINT trong PostgreSQL
    status: Optional[RestaurantStatusEnum] = RestaurantStatusEnum.inactive  # Trạng thái nhà hàng

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class RestaurantCreate(RestaurantBase):
    pass  # Khi tạo mới nhà hàng

class RestaurantUpdate(RestaurantBase):
    # Các thuộc tính có thể thay đổi khi cập nhật nhà hàng
    name: Optional[str] = None
    category: Optional[CategoryEnum] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    coord: Optional[str] = None
    status: Optional[RestaurantStatusEnum] = None

class Restaurant(RestaurantBase):
    restaurant_id: int  # ID nhà hàng
    merchant_id: int  # ID nhà cung cấp

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models


# ------------------------------
# Mô hình Thời gian hoạt động của nhà hàng
# ------------------------------

class DayEnum(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class RestaurantTimeBase(BaseModel):
    day: DayEnum  # Ngày trong tuần
    open_time: time  # Giờ mở cửa
    close_time: time  # Giờ đóng cửa

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class RestaurantTimeCreate(RestaurantTimeBase):
    pass  # Tạo mới thời gian hoạt động

class RestaurantTimeUpdate(RestaurantTimeBase):
    pass  # Cập nhật thời gian hoạt động

class RestaurantTimeResponse(RestaurantTimeBase):
    restaurant_id: int  # ID nhà hàng


# ------------------------------
# Mô hình Menu Item (Món ăn trong menu)
# ------------------------------

from models.models import ItemStatusEnum

class MenuItemBase(BaseModel):
    name: str  # Tên món ăn
    img_url: Optional[str] = None  # URL ảnh món ăn, có thể rỗng
    description: Optional[str] = None  # Mô tả món ăn, có thể rỗng
    price: Decimal  # Giá món ăn
    status: Optional[ItemStatusEnum] = ItemStatusEnum.unavailable  # Trạng thái món ăn (có sẵn hay không)
    is_deleted: Optional[bool] = False  # Trạng thái xóa món ăn, mặc định là False

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class MenuItemCreate(MenuItemBase):
    restaurant_id: int  # ID nhà hàng chứa món ăn

class MenuItemUpdate(MenuItemBase):
    pass  # Cập nhật món ăn

class MenuItem(MenuItemBase):
    item_id: int  # ID món ăn


# ------------------------------
# Mô hình Driver (Tài xế giao hàng)
# ------------------------------

class DriverStatusEnum(str, Enum):
    active = "active"  # Tài xế hoạt động
    inactive = "inactive"  # Tài xế không hoạt động

class DriverBase(BaseModel):
    name: str  # Tên tài xế
    status: DriverStatusEnum = DriverStatusEnum.inactive  # Trạng thái tài xế, mặc định là không hoạt động

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class DriverCreate(DriverBase):
    pass  # Tạo mới tài xế

class Driver(DriverBase):
    driver_id: int  # ID tài xế
    is_deleted: bool = False  # Trạng thái xóa tài xế


# ------------------------------
# Mô hình Admin (Quản trị viên)
# ------------------------------

class AdminBase(BaseModel):
    name: str  # Tên quản trị viên

    class Config:
        from_attributes  = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class AdminCreate(AdminBase):
    pass  # Tạo mới quản trị viên

class Admin(AdminBase):
    admin_id: int  # ID quản trị viên


# ------------------------------
# Mô hình Customer (Khách hàng)
# ------------------------------

class CustomerBase(BaseModel):
    name: str  # Tên khách hàng
    is_deleted: bool = False  # Trạng thái xóa khách hàng

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class CustomerCreate(CustomerBase):
    pass  # Tạo mới khách hàng

class Customer(CustomerBase):
    customer_id: int  # ID khách hàng


# ------------------------------
# Mô hình Order (Đơn hàng)
# ------------------------------

class OrderStatusEnum(str, Enum):
    cart = "cart"  # Đơn hàng trong giỏ
    pending = "pending"  # Đơn hàng đang chờ xử lý
    preparing = "preparing"  # Đơn hàng đang chuẩn bị
    delivering = "delivering"  # Đơn hàng đang giao
    delivered = "delivered"  # Đơn hàng đã giao
    completed = "completed"  # Đơn hàng đã hoàn thành
    cancelled = "cancelled"  # Đơn hàng đã hủy

class OrderBase(BaseModel):
    customer_id: int  # ID khách hàng
    restaurant_id: int  # ID nhà hàng
    driver_id: Optional[int] = None  # ID tài xế, có thể rỗng
    address: Optional[str] = None  # Địa chỉ giao hàng, có thể rỗng
    coord: Optional[str] = None  # Tọa độ giao hàng
    delivery_fee: Optional[float] = None  # Phí giao hàng
    food_fee: Optional[float] = None  # Phí món ăn
    order_status: OrderStatusEnum = OrderStatusEnum.cart  # Trạng thái đơn hàng
    note: Optional[str] = None  # Ghi chú

class OrderCreate(OrderBase):
    pass  # Tạo đơn hàng mới

class OrderUpdate(OrderBase):
    order_status: OrderStatusEnum  # Cập nhật trạng thái đơn hàng

class Order(OrderBase):
    order_id: int  # ID đơn hàng
    created_at: datetime  # Thời gian tạo đơn hàng
    delivered_at: Optional[datetime] = None  # Thời gian giao đơn hàng

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models


# ------------------------------
# Mô hình Order Item (Món trong đơn hàng)
# ------------------------------

class OrderItemBase(BaseModel):
    item_id: int  # ID món ăn
    order_id: int  # ID đơn hàng
    price: float  # Giá món ăn
    quantity: int = 1  # Số lượng món ăn, mặc định là 1

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class OrderItemCreate(OrderItemBase):
    pass  # Tạo món ăn trong đơn hàng

class OrderItem(OrderItemBase):
    pass  # Món ăn trong đơn hàng


# ------------------------------
# Mô hình Manager (Quản lý nhà hàng)
# ------------------------------

class ManagerBase(BaseModel):
    username: str  # Tên người dùng của quản lý
    name: str  # Tên quản lý
    restaurant_id: int  # ID nhà hàng quản lý

    class Config:
        from_attributes = True  # Chuyển đổi từ SQLAlchemy models sang Pydantic models

class ManagerCreate(ManagerBase):
    password: str  # Mật khẩu khi tạo quản lý mới

class Manager(ManagerBase):
    manager_id: int  # ID quản lý
