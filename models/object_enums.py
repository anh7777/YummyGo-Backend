from enum import Enum
# -------------------------
# Định nghĩa các ENUM
# -------------------------

class RoleEnum(str, Enum):
    customer = "customer"
    driver = "driver"
    restaurant = "restaurant"
    
# Trạng thái của tài xế
class DriverStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

# Trạng thái của nhà hàng
class RestaurantStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

# Trạng thái của món ăn
class ItemStatusEnum(str, Enum):
    available = "available"
    unavailable = "unavailable"

# Các ngày trong tuần
class DayEnum(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

# Trạng thái của đơn hàng
class OrderStatusEnum(str, Enum):
    cart = "cart"
    pending = "pending"
    preparing = "preparing"
    delivering = "delivering"
    delivered = "delivered"
    completed = "completed"
    cancelled = "cancelled"

# Các danh mục nhà hàng
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