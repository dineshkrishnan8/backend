from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserDtls
from uuid import uuid4

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user using JSON body { email, password }.

    Returns a simple token on success. In a production app replace the
    token generation with a signed JWT and secure password hashing.
    """
    user = db.query(UserDtls).filter(UserDtls.emailid == data.email).first()
    if not user or user.pwd != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid4())
    return {"message": "Login successful", "token": token}