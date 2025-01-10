from fastapi import Request, HTTPException

async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token or token != "your_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await call_next(request)
    return response
