from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationInfo
from decimal import Decimal
from typing import Optional
from datetime import datetime



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




class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username for registering")
    email: str = Field(..., max_length=250, description="username for registering")
    password: str = Field(..., max_length=150, description="the password of the user")
    confirm_password: str = Field(
        ..., max_length=150, description="the confirm password that user insert"
    )

    @field_validator("confirm_password")
    @classmethod
    def validate_password_input(cls, confirm_password: str, info: ValidationInfo):
        if not confirm_password or confirm_password != info.data.get("password"):
            raise ValueError("password does not match")
        return confirm_password


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username for registering")
    password: str = Field(..., max_length=150, description="the password of the user")
