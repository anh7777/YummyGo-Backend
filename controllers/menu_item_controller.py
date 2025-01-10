from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models import schemas
from services.menu_item_service import (
    create_menu_item,
    list_menu_items,
    get_menu_item,
    update_menu_item,
    delete_menu_item,
)

router = APIRouter(prefix="/menu_items", tags=["Menu Items"])

@router.post("/", response_model=schemas.MenuItem)
async def create_menu(menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return create_menu_item(menu_item, db)

@router.get("/", response_model=List[schemas.MenuItem])
async def get_all_menu_items(db: Session = Depends(get_db)):
    return list_menu_items(db)

@router.get("/{item_id}", response_model=schemas.MenuItem)
async def get_single_menu_item(item_id: int, db: Session = Depends(get_db)):
    return get_menu_item(item_id, db)

@router.put("/{item_id}", response_model=schemas.MenuItem)
async def update_menu(item_id: int, menu_item: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    return update_menu_item(item_id, menu_item, db)

@router.delete("/{item_id}")
async def remove_menu_item(item_id: int, db: Session = Depends(get_db)):
    return delete_menu_item(item_id, db)
