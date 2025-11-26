from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Store
from app.schemas import ProductSchema, StoreSchema

router = APIRouter()

@router.get("/combineddetails")
def get_combined_details(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    stores = db.query(Store).all()

    product_list = [ProductSchema.model_validate(p) for p in products]
    store_list = [StoreSchema.model_validate(s) for s in stores]

    return {
        "productSummary": len(products),
        "storeSummary": len(stores),
        "products": product_list,
        "stores": store_list
    }
