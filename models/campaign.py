from sqlalchemy import Column, String, Integer, Text, Date, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.user import User
from db.database import Base
from sqlalchemy import DateTime

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    country = Column(String, default="Nigeria", nullable=False)
    state = Column(String, nullable=False)
    school = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    story = Column(Text, nullable=False)
    cover_photo = Column(String, nullable=True)
    target_date = Column(DateTime, nullable=False)
    tags = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="campaigns")
