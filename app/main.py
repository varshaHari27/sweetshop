from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, database, auth, crud

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sweet Shop API", version="0.1.0")

get_db = database.get_db

# ------------------ Root ------------------ #
@app.get("/")
def read_root():
    return {"message": "Welcome to Sweet Shop API"}

# ------------------ Auth ------------------ #
@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------ Sweet CRUD ------------------ #
@app.post("/api/sweets", response_model=schemas.SweetResponse, status_code=201)
def add_sweet(sweet: schemas.SweetCreate, db: Session = Depends(get_db)):
    return crud.create_sweet(db, sweet)

@app.get("/api/sweets", response_model=list[schemas.SweetResponse])
def list_sweets(db: Session = Depends(get_db)):
    return crud.get_sweets(db)

@app.get("/api/sweets/{sweet_id}", response_model=schemas.SweetResponse)
def get_sweet(sweet_id: int, db: Session = Depends(get_db)):
    db_sweet = crud.get_sweet_by_id(db, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return db_sweet

@app.put("/api/sweets/{sweet_id}", response_model=schemas.SweetResponse)
def update_sweet(sweet_id: int, sweet: schemas.SweetCreate, db: Session = Depends(get_db)):
    return crud.update_sweet(db, sweet_id, sweet)

# ------------------ Admin-protected endpoints ------------------ #
@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(sweet_id: int, 
                 db: Session = Depends(get_db), 
                 current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.delete_sweet(db, sweet_id)

@app.post("/api/sweets/{sweet_id}/restock", response_model=schemas.SweetResponse)
def restock_sweet(sweet_id: int, 
                  quantity: int = 1, 
                  db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.restock_sweet(db, sweet_id, quantity)

# ------------------ Purchase ------------------ #
@app.post("/api/sweets/{sweet_id}/purchase", response_model=schemas.SweetResponse)
def purchase_sweet(sweet_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    return crud.purchase_sweet(db, sweet_id, quantity)

# ------------------ Search ------------------ #
@app.get("/api/sweets/search", response_model=list[schemas.SweetResponse])
def search_sweets_endpoint(
    name: str = Query(None, description="Name of the sweet"),
    category: str = Query(None, description="Category of the sweet"),
    min_price: int = Query(None, ge=0, description="Minimum price"),
    max_price: int = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db)
):
    return crud.search_sweets(db, name, category, min_price, max_price)
