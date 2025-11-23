# from sqlalchemy import Column, Integer, BigInteger, String, Date, DECIMAL, Boolean, ForeignKey
# from .database import Base

# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True, index=True)
#     sku = Column(String(100), unique=True)
#     name = Column(String(255))
#     category = Column(String(100))

# class Store(Base):
#     __tablename__ = "stores"
#     id = Column(Integer, primary_key=True, index=True)
#     store_code = Column(String(50))
#     name = Column(String(255))
#     region = Column(String(100))

# class Sale(Base):
#     __tablename__ = "sales"
#     id = Column(BigInteger, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))
#     store_id = Column(Integer, ForeignKey("stores.id"))
#     sale_date = Column(Date)
#     quantity = Column(Integer)
#     price = Column(DECIMAL(10,2))
#     promo_flag = Column(Boolean)

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), nullable=False)
    name = Column(String(255))
    category = Column(String(100))


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_code = Column(String(50))
    name = Column(String(255))
    region = Column(String(100))


class Sales(Base):
    __tablename__ = "sales"

    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    sale_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    promo_flag = Column(Boolean, default=False)
    created_on = Column(DateTime, server_default=func.now())

class UserDtls(Base): 
    __tablename__ = "user_dtls" 
     
    id = Column("userid", Integer, primary_key=True, index=True)  # Python: id, DB: userid
    emailid = Column(String(255), unique=True, nullable=False) 
    pwd = Column(String(255), nullable=False)


    
