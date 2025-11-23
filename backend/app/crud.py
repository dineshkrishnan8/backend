from sqlalchemy.orm import Session
from app.models import Sales
from datetime import timedelta
import pandas as pd
from app.models import UserDtls


# ---------------------------
# Get ALL sales
# ---------------------------
def get_sales(db: Session):
    return db.query(Sales).all()


def get_all_users(db: Session):
    return db.query(UserDtls).all()


# ---------------------------
# Get sale by ID
# ---------------------------
def get_sale_by_id(db: Session, sale_id: int):
    return db.query(Sales).filter(Sales.id == sale_id).first()


# ---------------------------
# Create new sale
# ---------------------------
def create_sale(db: Session, sale_data):
    new_sale = Sales(
        product_id=sale_data.product_id,
        store_id=sale_data.store_id,
        quantity=sale_data.quantity,
        price=sale_data.price,
        sale_date=sale_data.sale_date,
        promo_flag=sale_data.promo_flag
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


# ---------------------------
# SALES BY PRODUCT + STORE
# ---------------------------
def get_sales_by_product_store(db: Session, product_id: int, store_id: int):
    return (
        db.query(Sales)
        .filter(Sales.product_id == product_id, Sales.store_id == store_id)
        .order_by(Sales.sale_date)
        .all()
    )




# ---------------------------
# Convert Sales to DataFrame (for forecasting)
# ---------------------------
def get_sales_df(db: Session, product_id: int, store_id: int):
    rows = get_sales_by_product_store(db, product_id, store_id)
    if not rows:
        return pd.DataFrame()

    data = [
        {
            "sale_date": r.sale_date,
            "quantity": r.quantity,
            "price": r.price,
            "promo_flag": r.promo_flag,
        }
        for r in rows
    ]

    df = pd.DataFrame(data)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df


def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_all_stores(db: Session):
    return db.query(models.Store).all()