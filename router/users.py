from fastapi import APIRouter, Depends
from schemas.users import UserCreate, UserDisplay, ForgotPasswordRequest, ResetPasswordRequest, UserLogin
from sqlalchemy.orm import Session
from db.database import get_db
from services.users import create_user, get_all_users, forgot_password, reset_password, delete_user, update_user, login_user, reset_password_direct, refresh_access_token, logout
from typing import List, Dict
from auth.oauth2 import get_current_user
from models.user import User
from auth.oauth2 import bearer_scheme
from fastapi.security import HTTPAuthorizationCredentials


router = APIRouter()
 
# Create User
@router.post('/', response_model=UserDisplay)
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, request)

# Read all User
@router.get('/', response_model=List[UserDisplay])
def get_all_user(db: Session = Depends(get_db),  current_user:UserCreate=Depends(get_current_user)):
    return get_all_users(db, current_user)

# Update User
# @router.post('/{id}/update')
# def update_a_user(id: int, request: UserCreate, db: Session=Depends(get_db),  current_user:UserBase=Depends(get_current_user)):
#     return update_user(db, id, request)

# # Delete User
# @router.get('/delete/{id}')
# def delete(id: int, db: Session=Depends(get_db),  current_user:UserBase=Depends(get_current_user)):
#     return delete_user(db, id)

@router.post('/forgot-password')
def forgot_password_route(request: ForgotPasswordRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    return forgot_password(db, request.email)

@router.post('/reset-password')
def reset_forgotten_password(request: ResetPasswordRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    return reset_password(db, request.token, request.new_password)

@router.post("/reset-password-direct")
def reset_password_directly(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # user must be logged in
):
    return reset_password_direct(db, current_user, old_password, new_password)

@router.post('/login')
def login(request: UserLogin, db: Session = Depends(get_db)):
    return login_user(request, db)


@router.post("/logout")
def logout_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    return logout(db, credentials)


@router.post("/refresh")
def refresh(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    return refresh_access_token(db, credentials)