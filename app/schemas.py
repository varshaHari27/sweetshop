from pydantic import BaseModel, ConfigDict

# ---------------- User ----------------
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)  # replaces class Config with orm_mode

# ---------------- Auth Token ----------------
class Token(BaseModel):
    access_token: str
    token_type: str

# ---------------- Sweets ----------------
class SweetCreate(BaseModel):
    name: str
    category: str
    price: int
    quantity: int

class SweetResponse(SweetCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
