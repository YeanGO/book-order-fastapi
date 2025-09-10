from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class OrderBase(BaseModel):
    buyer_name: str = Field(min_length=1, max_length=100)
    book_title: str = Field(min_length=1, max_length=200)
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(ge=0)
    note: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    buyer_name: Optional[str] = None
    book_title: Optional[str] = None
    quantity: Optional[int] = Field(default=None, ge=1)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)
    note: Optional[str] = None

class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
