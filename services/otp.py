from datetime import datetime, timedelta
import random
from models.otp import OTP
from models.user import User
from sqlalchemy.orm import Session
from services.email import send_otp_email

def generate_otp(db: Session, user_id: str, expiry_minutes: int = 5):
    # check if user has an active OTP
    existing_otp = db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.is_used == False,
        OTP.expires_at > datetime.utcnow()
    ).first()

    if existing_otp:
        return existing_otp  # still valid, return same OTP

    # otherwise, create a new OTP
    new_otp = OTP(
        user_id=user_id,
        otp=str(random.randint(100000, 999999)),  # 6-digit code
        expires_at=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return new_otp

def send_verification_otp(db: Session, user):
    otp = generate_otp(db, user.id)
    send_otp_email(user.email, otp.otp) 
    return {"message": "OTP sent to email"}

def verify_otp(db: Session, user_id: str, otp_code: str):
    otp = db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.otp == otp_code,
        OTP.is_used == False
    ).first()

    if not otp:
        return {"error": "Invalid OTP"}

    if otp.expires_at < datetime.utcnow():
        return {"error": "OTP expired"}

    otp.is_used = True
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user.is_verified = True
    db.commit()
    return {"message": "OTP verified successfully"}




def otp_expiry(minutes: int = 5):
    return datetime.utcnow() + timedelta(minutes=minutes)
