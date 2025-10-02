from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas.users import UserCreate, UserLogin
from models.user import User 
from models.tokens import RefreshToken
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status
from services.otp import generate_otp, otp_expiry
from services.email import send_otp_email, send_reset_password_email
from datetime import datetime, timedelta
import uuid
from auth.oauth2 import create_access_token, create_refresh_token, verify_refresh_token, decode_access_token
# from auth.authentication import get_token


def create_user(db: Session, request: UserCreate):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        ) 
    new_user = User(
        username = request.username,
        email = request.email,
        hashed_password = Hash.bcrypt(request.password),
        otp_expiry = otp_expiry()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    otp = generate_otp(db, new_user.id)
    try:
        send_otp_email(request.email, otp.otp)
    except Exception as e:
        raise HTTPException(500, f"Failed to send OTP email: {str(e)}")
    return new_user

def get_all_users(db: Session, user:User):
    return db.query(User).all()

def update_user(db: Session, id: int, request: UserCreate):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = f'User with {id} not found')
    user.update({
        User.username: request.username,
        User.email: request.email,
        User.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'ok'

def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = f'User with {id} not found')
    db.delete(user)
    db.commit()
    return 'has been deleted'

def forgot_password(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )
    

    reset_token = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(minutes=30)  

    user.reset_token = reset_token
    user.reset_token_expiry = expiry
    db.commit()
    db.refresh(user)

    # Send reset link via email
    reset_link = f"http://localhost:8000/auth/reset-password?token={reset_token}"
    try:
        send_reset_password_email(email, reset_link)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send reset email: {str(e)}"
        )
    
    return {"message": "Password reset link sent to your email"}



def reset_password(db: Session, token: str, new_password: str):
    user = db.query(User).filter(User.reset_token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    if not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    user.hashed_password = Hash.bcrypt(new_password)

    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()
    db.refresh(user)

    return {"message": "Password reset successful"}

def reset_password_direct(db: Session, user: User, old_password: str, new_password: str):
    if not Hash.verify(old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )
    
    user.hashed_password = Hash.bcrypt(new_password)
    db.commit()
    db.refresh(user)
    return {"msg": "Password updated successfully"}


def authenticate_user(db: Session, request: UserLogin):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified. Please verify OTP first.")
    if not Hash.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(user, db)

    return user, {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def login_user(request: UserLogin, db: Session ):
    user, tokens = authenticate_user(db, request)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        **tokens
    }

def refresh_access_token(db: Session, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    db_token = verify_refresh_token(token, db)

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_access_token = create_access_token({"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}


def logout(db: Session, credentials: HTTPAuthorizationCredentials ):
    access_token = credentials.credentials
    payload = decode_access_token(access_token)
    user_id = payload.get("sub")

    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()
    return {"message": "Logged out successfully"}