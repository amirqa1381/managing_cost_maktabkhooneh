from pydantic import BaseModel, Field, field_validator
from typing import Optional


class CostBaseModel(BaseModel):
    description: str = Field(..., description="field for manage the description of each cost")
    amount : float | int = Field(..., description="amount that user should insert and it can be int or float")
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, value: str):
        if len(value) > 100:
            raise ValueError("Length of the description should not be exceed 100")
    
    
class CostCreateModel(CostBaseModel):
    pass

class CostReadModel(CostBaseModel):
    id : int = Field(..., description="the identity field and it is created automatically")


class CostUpdateModel(BaseModel):
    description: Optional[str] = Field(None, description="optional description for update")
    amount: Optional[int | float] = Field(None, description="optional amount for update")