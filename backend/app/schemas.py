from pydantic import BaseModel
from datetime import date


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

    model_config = {"from_attributes": True}   


class ForecastPoint(BaseModel):
    date: date
    predicted_quantity: float


class UserDtls(BaseModel):
    id: int
    emailid: str
    pwd: str

    model_config = {"from_attributes": True}


class ProductSchema(BaseModel):
    id: int
    sku: str
    name: str
    category: str

    model_config = {"from_attributes": True}  


class StoreSchema(BaseModel):
    id: int
    store_code: str
    name: str
    region: str

    model_config = {"from_attributes": True}  
