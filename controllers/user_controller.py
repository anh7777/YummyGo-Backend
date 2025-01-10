from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from services import user_service
from models import schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_service.create_user_service(user, db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_service.get_user_service(user_id, db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[schemas.User])
async def list_users(db: Session = Depends(get_db)):
    return user_service.list_users_service(db)

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = user_service.update_user_service(user_id, user, db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        message = user_service.delete_user_service(user_id, db)
        return {"detail": message}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
