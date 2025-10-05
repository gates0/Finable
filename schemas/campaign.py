from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional

class CampaignBase(BaseModel):
    state: str
    school: str
    currency: str
    amount: float
    story: str
    title: str
    target_date: date
    tags: Optional[str] = None

    @field_validator("target_date", mode="before")
    def parse_date(cls, v):
        if isinstance(v, str):
            # Try multiple formats
            for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
        elif isinstance(v, datetime):
            return v.date()
        return v

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    state: Optional[str] = None
    school: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[float] = None
    story: Optional[str] = None
    title: Optional[str] = None
    target_date: Optional[date] = None
    tags: Optional[str] = None


class CampaignOut(CampaignBase):
    id: int
    country: str
    user_id: str
    cover_photo: str

    class Config:
        orm_mode = True
