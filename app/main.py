from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, auth
from .database import engine, Base, get_db

# ---------------- FastAPI app ----------------
app = FastAPI(title="Sweet Shop Management System")

# ---------------- CORS ----------------
origins = [
    "http://localhost:5173",  # Vite frontend URL
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Create DB Tables ----------------
Base.metadata.create_all(bind=engine)

# ---------------- Root ----------------
@app.get("/")
def root():
    return {"message": "Welcome to the Sweet Shop API!"}

# ---------------- User Auth ----------------
@app.post("/api/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------- Sweets ----------------
@app.get("/api/sweets/search", response_model=List[schemas.SweetResponse])
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Sweet)
    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Sweet.price <= max_price)
    return query.all()

@app.post("/api/sweets", response_model=schemas.SweetResponse)
def create_sweet(sweet: schemas.SweetCreate, db: Session = Depends(get_db)):
    new_sweet = models.Sweet(**sweet.model_dump())
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet

@app.get("/api/sweets", response_model=List[schemas.SweetResponse])
def list_sweets(db: Session = Depends(get_db)):
    return db.query(models.Sweet).all()

@app.get("/api/sweets/{sweet_id}", response_model=schemas.SweetResponse)
def get_sweet(sweet_id: int, db: Session = Depends(get_db)):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return sweet

@app.put("/api/sweets/{sweet_id}", response_model=schemas.SweetResponse)
def update_sweet(sweet_id: int, sweet: schemas.SweetCreate, db: Session = Depends(get_db)):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    for key, value in sweet.model_dump().items():
        setattr(db_sweet, key, value)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(sweet_id: int, db: Session = Depends(get_db)):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db.delete(sweet)
    db.commit()
    return {"message": "Sweet deleted successfully"}

# ---------------- Inventory ----------------
@app.post("/api/sweets/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int, db: Session = Depends(get_db)):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")
    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)
    return {"message": f"Purchased {sweet.name}. Remaining stock: {sweet.quantity}"}

@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(sweet_id: int, amount: int = 10, db: Session = Depends(get_db)):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    sweet.quantity += amount
    db.commit()
    db.refresh(sweet)
    return {"message": f"Restocked {sweet.name}. New stock: {sweet.quantity}"}
