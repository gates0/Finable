from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.otp import send_verification_otp, verify_otp
from models.user import User
from schemas.otp import OTPVerify

router = APIRouter()

@router.post("/send/{user_id}")
def send_otp(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    return send_verification_otp(db, user)

@router.post("/verify")
def verify_otp_code(request: OTPVerify, db: Session = Depends(get_db)):
    return verify_otp(db, request.user_id, request.otp)
