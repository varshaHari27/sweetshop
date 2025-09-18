from fastapi import FastAPI
from database import engine, Base

# Import models (we’ll create this next)
import models

# Create all tables (only for dev; migrations are better in production)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to SweetShop API 🎉"}
