from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException

def create_admin(admin: schemas.AdminCreate, db: Session):
    """
    Tạo một admin mới. Kiểm tra nếu admin đã tồn tại, trả về lỗi.
    """
    # Kiểm tra xem admin đã tồn tại hay chưa
    db_admin = db.query(models.Admin).filter(models.Admin.name == admin.name).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Admin đã tồn tại")

    # Tạo đối tượng Admin mới
    new_admin = models.Admin(name=admin.name)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin

def get_admin(admin_id: int, db: Session):
    """
    Lấy thông tin admin theo ID. Trả về lỗi nếu admin không tồn tại.
    """
    db_admin = db.query(models.Admin).filter(models.Admin.admin_id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin không tồn tại")
    return db_admin
