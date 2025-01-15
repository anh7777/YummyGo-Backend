from fastapi import FastAPI
from routes.api_router import api_router
import sys
sys.path.append("d:/yummygo/backend")
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Application")

origins = [
    "http://localhost:3000",  # Thêm domain frontend của bạn
    "http://localhost",  # Nếu frontend và backend cùng chạy trên localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép chia sẻ cookie giữa các domain
    allow_credentials=True,  # Bật gửi cookies trong các yêu cầu
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký tất cả router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI application!"}
