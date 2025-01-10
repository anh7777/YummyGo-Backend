from fastapi import FastAPI
from routes.api_router import api_router

app = FastAPI(title="FastAPI Application")

# Đăng ký tất cả router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI application!"}
