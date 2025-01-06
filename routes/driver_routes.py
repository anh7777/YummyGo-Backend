from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.database import get_db
from models.models import Driver

router = APIRouter()

@router.get("/")
def get_drivers(db: Session = Depends(get_db)):
    return db.query(Driver).all()

@router.post("/")
def create_driver(driver: dict, db: Session = Depends(get_db)):
    new_driver = Driver(
        name=driver["name"],
        phone=driver["phone"],
        vehicle_type=driver.get("vehicle_type", ""),
        license_plate=driver.get("license_plate", "")
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

@router.get("/{driver_id}")
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.put("/{driver_id}")
def update_driver(driver_id: int, updated_data: dict, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    for key, value in updated_data.items():
        setattr(driver, key, value)
    
    db.commit()
    db.refresh(driver)
    return driver

@router.delete("/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    db.delete(driver)
    db.commit()
    return {"message": "Driver deleted successfully"}
