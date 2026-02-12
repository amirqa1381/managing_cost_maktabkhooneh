from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal
from typing import Optional


class CostBase(BaseModel):
    description: str = Field(..., max_length=255)
    amount: Decimal = Field(..., gt=0)


class CostCreate(CostBase):
    user_id: int = Field(..., gt=0)


class CostUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0)


class CostRead(CostBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)




class UserBase(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    id: int
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)