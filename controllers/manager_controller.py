from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import schemas
from db.database import get_db
from services.manager_service import (
    create_manager_service,
    get_manager_service,
    update_manager_service,
    delete_manager_service,
)

router = APIRouter(prefix="/divers", tags=["Drivers"])

# Route POST để tạo mới Manager
@router.post("/", response_model=schemas.Manager)
async def create_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db)):
    return create_manager_service(manager, db)

# Route GET để lấy thông tin Manager
@router.get("/{manager_id}", response_model=schemas.Manager)
async def get_manager(manager_id: int, db: Session = Depends(get_db)):
    return get_manager_service(manager_id, db)

# Route PUT để cập nhật thông tin Manager
@router.put("/{manager_id}", response_model=schemas.Manager)
async def update_manager(manager_id: int, manager: schemas.ManagerCreate, db: Session = Depends(get_db)):
    return update_manager_service(manager_id, manager, db)

# Route DELETE để xóa Manager
@router.delete("/{manager_id}")
async def delete_manager(manager_id: int, db: Session = Depends(get_db)):
    return delete_manager_service(manager_id, db)
