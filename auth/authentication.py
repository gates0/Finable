from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from models.user import User 
from models.otp import OTP
from schemas.users import UserLogin
from db.hash import Hash
from auth.oauth2 import create_access_token, create_refresh_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime
from services.users import authenticate_user

router = APIRouter(
    tags=['authentication']
)

# @router.post('/tokens')
def get_token(request: UserLogin, db: Session = Depends(get_db)):
    _, tokens = authenticate_user(db, request)
    return tokens

