from fastapi import WebSocket, WebSocketDisconnect, APIRouter, HTTPException
from services.connection_manager import ConnectionManager
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from services.order_service import *
from db.database import get_db
from services.connection_manager import ConnectionManager

router = APIRouter(prefix="/ws", tags=["WebSocket"])

manager = ConnectionManager()

# WebSocket for drivers
@router.websocket("/drivers/{driver_id}")
async def websocket_driver(websocket: WebSocket, driver_id: int):
    await manager.connect(websocket, "drivers", driver_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from driver {driver_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect("drivers", driver_id)
        print(f"Driver {driver_id} disconnected")

# WebSocket for customers
@router.websocket("/customers/{customer_id}")
async def websocket_customer(websocket: WebSocket, customer_id: int):
    await manager.connect(websocket, "customers", customer_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from customer {customer_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect("customers", customer_id)
        print(f"Customer {customer_id} disconnected")

# WebSocket for restaurants
@router.websocket("/restaurants/{restaurant_id}")
async def websocket_restaurant(websocket: WebSocket, restaurant_id: int):
    await manager.connect(websocket, "restaurants", restaurant_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from restaurant {restaurant_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect("restaurants", restaurant_id)
        print(f"Restaurant {restaurant_id} disconnected")

# API /send-message

# server gửi cho nhà hàng khi có đơn hàng mới
# Kết nối WebSocket cho nhà hàng
@router.websocket("/ws/restaurant/{restaurant_id}")
async def websocket_endpoint_for_restaurant(websocket: WebSocket, restaurant_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Data from restaurant: {data}")
    except WebSocketDisconnect:
        manager.connections["restaurants"][restaurant_id].remove(websocket)

# Kết nối WebSocket cho tài xế
@router.websocket("/ws/driver/{driver_id}")
async def websocket_endpoint_for_driver(websocket: WebSocket, driver_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Data from driver: {data}")
    except WebSocketDisconnect:
        manager.connections["drivers"][driver_id].remove(websocket)

