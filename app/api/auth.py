from fastapi import APIRouter, HTTPException
from api.schemas import LoginRequest

router = APIRouter()

@router.post("/login")
def login(data: LoginRequest):
    if data.username != "admin" or data.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": "fake-jwt-token"}