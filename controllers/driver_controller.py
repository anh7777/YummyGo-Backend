from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models import schemas
from services.driver_service import (
    create_driver_service,
    list_drivers_service,
    get_driver_service,
    update_driver_service,
    delete_driver_service,
)

router = APIRouter(prefix="/drivers", tags=["Drivers"])

# ------------------------------
# Quản lý Tài Xế (Controller)
# ------------------------------

@router.post("/", response_model=schemas.Driver)
async def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    return create_driver_service(driver, db)


@router.get("/", response_model=List[schemas.Driver])
async def list_drivers(db: Session = Depends(get_db)):
    return list_drivers_service(db)


@router.get("/{driver_id}", response_model=schemas.Driver)
async def get_driver(driver_id: int, db: Session = Depends(get_db)):
    return get_driver_service(driver_id, db)


@router.put("/{driver_id}", response_model=schemas.Driver)
async def update_driver(driver_id: int, driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    return update_driver_service(driver_id, driver, db)


@router.delete("/{driver_id}", response_model=schemas.Driver)
async def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    return delete_driver_service(driver_id, db)
