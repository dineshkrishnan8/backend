# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.models import UserDtls

# router = APIRouter()

# # Request and Response models
# class LoginRequest(BaseModel):
#     email: str
#     password: str

# class LoginResponse(BaseModel):
#     message: str
#     success: bool

# # Database dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Login endpoint
# # @router.post("/login", response_model=LoginResponse)
# # def login(data: LoginRequest, db: Session = Depends(get_db)):
# #     user = db.query(UserDtls).filter(UserDtls.emailid == data.email).first()
# #     if not user or user.pwd != data.password:
# #         raise HTTPException(status_code=401, detail="Incorrect email or password")
# #     return {"message": "Login successful", "success": True}


# router = APIRouter()

# @router.post("/login", response_model=LoginResponse)
# def login(data: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(UserDtls).filter(UserDtls.emailid == data.email).first()
#     if not user or user.pwd != data.password:
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
#     return {"message": "Login successful", "success": True}



from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import UserDtls

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    success: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/login", response_model=LoginResponse)
# def login(data: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(UserDtls).filter(UserDtls.emailid == data.email).first()
#     if not user or user.pwd != data.password:
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
#     return {"message": "Login successful", "success": True}


# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserDtls

router = APIRouter()

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserDtls).filter(UserDtls.emailid == email).first()
    if not user or user.pwd != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}