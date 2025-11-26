from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
from app.routes import auth
from app.routes import all_details
from app.database import SessionLocal, engine
from app import models, crud, schemas, forecast
from app.routes import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FMCG Sales Forecast API")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(all_details.router, prefix="/dtls", tags=["auth"])

@app.get("/")
def home():
    return {"message": "API is running!"}


@app.get("/users", response_model=list[schemas.UserDtls])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users

@app.get("/stores/{store_id}", response_model=schemas.StoreSchema)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@app.get("/products/{product_id}", response_model=schemas.ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/sales", response_model=list[schemas.Sale])
def get_all_sales(db: Session = Depends(get_db)):
    return crud.get_sales(db)

@app.get("/sales/{sale_id}", response_model=schemas.Sale)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = crud.get_sale_by_id(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@app.post("/sales", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)

@app.get("/sales/{product_id}/{store_id}", response_model=list[schemas.Sale])
def read_sales(product_id: int, store_id: int, db: Session = Depends(get_db)):
    rows = crud.get_sales_by_product_store(db, product_id, store_id)
    if not rows:
        raise HTTPException(status_code=404, detail="No sales found")
    return rows

@app.post("/forecast/{product_id}/{store_id}", response_model=list[schemas.ForecastPoint])
def get_forecast(product_id: int, store_id: int, days: int = 7, db: Session = Depends(get_db)):
    df = crud.get_sales_df(db, product_id, store_id)
    if df.empty:
        raise HTTPException(status_code=404, detail="No sales history found")
    model = forecast.train_model(df)
    preds = forecast.forecast_next_days(df, days=days, model=model)
    return preds

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload Excel file.")
    df = pd.read_excel(file.file)
    required_columns = {"product_id", "store_id", "sale_date", "quantity", "price", "promo_flag"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"Excel must contain: {required_columns}")
    for _, row in df.iterrows():
        sale = models.Sales(
            product_id=int(row["product_id"]),
            store_id=int(row["store_id"]),
            sale_date=pd.to_datetime(row["sale_date"]),
            quantity=int(row["quantity"]),
            price=float(row["price"]),
            promo_flag=bool(row.get("promo_flag", 0)),
        )
        db.add(sale)
    db.commit()
    return {"status": "success", "rows_inserted": len(df)}

from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
