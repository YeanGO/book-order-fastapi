from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

def list_orders(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(models.Order).order_by(models.Order.id.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_order(db: Session, order_id: int):
    return db.get(models.Order, order_id)

def create_order(db: Session, order: schemas.OrderCreate):
    obj = models.Order(**order.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_order(db: Session, order_id: int, payload: schemas.OrderUpdate):
    obj = db.get(models.Order, order_id)
    if not obj:
        return None
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_order(db: Session, order_id: int):
    obj = db.get(models.Order, order_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
