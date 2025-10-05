from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
# from .tokens import RefreshToken
# from .otp import OTP

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    otp_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

    otps = relationship("OTP", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")

   


