from typing import Dict, List
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.exceptions import HTTPException
from utils.access_token import decode_access_token

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, Dict[int, WebSocket]] = {
            "drivers": {},       # Tài xế
            "restaurants": {},   # Nhà hàng
            "customers": {},     # Khách hàng
        }

    async def connect(self, websocket: WebSocket, user_type: str, user_id: int):
        await websocket.accept()
        if user_type in self.connections:
            self.connections[user_type][user_id] = websocket
        else:
            await websocket.close()

    async def disconnect(self, user_type: str, user_id: int):
        if user_type in self.connections and user_id in self.connections[user_type]:
            del self.connections[user_type][user_id]
        else:
            print(f"User {user_id} not found in {user_type} connections.")
    
    async def cus_send_dri():
        pass
    
    async def cus_send_res():
        pass

    async def dri_send_cus():
        pass
    
    async def res_send_cus():
        pass
    
    async def dri_send_res():
        pass
    
    async def res_send_dri():
        pass
    
    async def broadcast_message(self, user_type: str, message: dict):
        if user_type in self.connections:
            for user_id, websocket in list(self.connections[user_type].items()):
                try:
                    await websocket.send_json(message)
                except WebSocketDisconnect:
                    # Nếu kết nối bị ngắt, hãy xóa người dùng khỏi danh sách
                    print(f"User {user_id} disconnected while broadcasting.")
                    self.disconnect(user_type, user_id)
        else:
            print(f"No connections found for user type {user_type}.")


    async def get_current_user(websocket: WebSocket):
        # Logic lấy token từ header hoặc cookie
        token = websocket.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Phân tích token và lấy thông tin người dùng
        user = decode_access_token(token)
        return user

