from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.user_controller import register_user
from utils.database import get_db

router = APIRouter()

@router.post("/auth/register")
def register(user: dict, db: Session = Depends(get_db)):
    return register_user(db, user)
