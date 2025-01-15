from middlewares.auth_middleware import get_current_user
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/logout")
async def logout(token: str = Depends(get_current_user)):

    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie(key="access_token")  # Xóa cookie 
    
    return response