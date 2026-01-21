from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserCreate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    
class UserResponse(BaseModel):
    
    id: int
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True
class UserLogin(BaseModel):
    email:str
    password:str    

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str

class CapitalInput(BaseModel):
    year: int = Field(..., ge=1900, le=2100, description="Year for predicting per capital income")

class CapitalResponse(BaseModel):
    predicted_income: float = Field(..., description="Predicted per capital income")
