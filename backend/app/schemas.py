from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class SaleBase(BaseModel):
    product_id: int
    store_id: int
    sale_date: date
    quantity: int
    price: float
    promo_flag: bool


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2 replacement for orm_mode


class ForecastPoint(BaseModel):
    date: date
    predicted_quantity: float


class UserDtls(BaseModel):
    id: int
    emailid: str
    pwd: str  # include password

    class Config:
        from_attributes = True
    
