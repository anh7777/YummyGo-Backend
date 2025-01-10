from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import schemas
from db.database import get_db
from services.admin_service import create_admin, get_admin

router = APIRouter(prefix="/admins", tags=["Admins"])

# Route POST: Tạo mới Admin
@router.post("/", response_model=schemas.Admin)
async def create_admin_route(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    """
    API để tạo một admin mới.
    """
    return create_admin(admin, db)

# Route GET: Lấy thông tin Admin theo admin_id
@router.get("/{admin_id}", response_model=schemas.Admin)
async def get_admin_route(admin_id: int, db: Session = Depends(get_db)):
    """
    API để lấy thông tin admin dựa trên admin_id.
    """
    return get_admin(admin_id, db)
