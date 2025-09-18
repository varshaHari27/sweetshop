from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status

# ------------------ Sweet CRUD ------------------ #

def get_sweets(db: Session):
    return db.query(models.Sweet).all()

def get_sweet_by_id(db: Session, sweet_id: int):
    return db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

def create_sweet(db: Session, sweet: schemas.SweetCreate):
    db_sweet = models.Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def update_sweet(db: Session, sweet_id: int, sweet: schemas.SweetCreate):
    db_sweet = get_sweet_by_id(db, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db_sweet.name = sweet.name
    db_sweet.category = sweet.category
    db_sweet.price = sweet.price
    db_sweet.quantity = sweet.quantity
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def delete_sweet(db: Session, sweet_id: int):
    db_sweet = get_sweet_by_id(db, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db.delete(db_sweet)
    db.commit()
    return {"detail": "Sweet deleted"}

# ------------------ Inventory Operations ------------------ #

def purchase_sweet(db: Session, sweet_id: int, quantity: int = 1):
    db_sweet = get_sweet_by_id(db, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if db_sweet.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    db_sweet.quantity -= quantity
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def restock_sweet(db: Session, sweet_id: int, quantity: int = 1):
    db_sweet = get_sweet_by_id(db, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db_sweet.quantity += quantity
    db.commit()
    db.refresh(db_sweet)
    return db_sweet
