# models/otp.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db.database import Base
import uuid
from models.user import User

class OTP(Base):
    __tablename__ = "otps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    otp = Column(String, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))
    is_used = Column(Boolean, default=False)

    user = relationship("User", back_populates="otps")
