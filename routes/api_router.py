from fastapi import APIRouter
from controllers.admin_controller import router as admin_router
from controllers.customer_controller import router as customer_router
from controllers.driver_controller import router as driver_router
from controllers.manager_controller import router as manager_router
from controllers.restaurant_controller import router as restaurant_router
from controllers.menu_item_controller import router as menu_item_router
from controllers.order_controller import router as order_router
from controllers.restaurant_controller import router as restaurant_router
from controllers.user_controller import router as user_router
from controllers.register_controller import router as register_router
from controllers.login_controller import router as login_router
from controllers.logout_controller import router as logout_router
# Tập hợp tất cả các router
api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(order_router)
api_router.include_router(admin_router)
api_router.include_router(customer_router)
api_router.include_router(driver_router)
api_router.include_router(manager_router)
api_router.include_router(restaurant_router)
api_router.include_router(menu_item_router)
api_router.include_router(login_router)
api_router.include_router(logout_router)
api_router.include_router(register_router)
