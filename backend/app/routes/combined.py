# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models import Product, Store
# router = APIRouter()

# @router.get("/combined-details")
# def get_combined_details(db: Session = Depends(get_db)):
#     products = db.query(Product).all()
#     stores = db.query(Store).all()

#     return {
#         "productSummary": len(products),
#         "storeSummary": len(stores),
#         "products": products,
#         "stores": stores
#     }