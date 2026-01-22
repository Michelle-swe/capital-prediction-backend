from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# User authentication schemas
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
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str


# Income prediction schemas
class IncomeRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100, description="Year for predicting per capita income")


class IncomeResponse(BaseModel):
    predicted_income: float = Field(..., description="Predicted per capita income")


# Aliases for backwards compatibility
class CapitalInput(IncomeRequest):
    pass


class CapitalResponse(IncomeResponse):
    pass
