from fastapi import APIRouter, Depends, Form, UploadFile, File, status
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List
from db.database import get_db
from auth.oauth2 import get_current_user
from models.user import User
from schemas.campaign import CampaignCreate, CampaignOut, CampaignUpdate
from services.campaign import create_campaign, get_all_campaigns, delete_campaign, update_campaign

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CampaignOut)
def create_new_campaign(
    state: str = Form(...),
    school: str = Form(...),
    currency: str = Form(...),
    amount: float = Form(...),
    story: str = Form(...),
    title: str = Form(...),
    target_date: date = Form(...),
    tags: Optional[str] = Form(None),
    cover_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign_data = CampaignCreate(
        state=state,
        school=school,
        currency=currency,
        amount=amount,
        story=story,
        title=title,
        target_date=target_date,
        tags=tags
    )

    new_campaign = create_campaign(
        db=db,
        current_user=current_user,
        campaign_data=campaign_data,
        cover_photo=cover_photo
    )
    return new_campaign

@router.put("/{campaign_id}")
def update_existing_campaign(
    campaign_id: int,
    state: str = Form(None),
    school: str = Form(None),
    currency: str = Form(None),
    amount: float = Form(None),
    story: str = Form(None),
    title: str = Form(None),
    target_date: str = Form(None),
    tags: str = Form(None),
    cover_photo: UploadFile = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = CampaignUpdate(
        state=state,
        school=school,
        currency=currency,
        amount=amount,
        story=story,
        title=title,
        target_date=target_date,
        tags=tags,
    )

    campaign = update_campaign(
        db=db,
        campaign_id=campaign_id,
        user_id=current_user.id,
        data=data,
        cover_photo=cover_photo,
    )
    return campaign

@router.get("/", response_model=List[CampaignOut])
def fetch_all_campaigns(db: Session = Depends(get_db)):
    campaigns = get_all_campaigns(db)
    return campaigns

@router.delete("/{campaign_id}", status_code=status.HTTP_200_OK)
def remove_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
):
    return delete_campaign(db, campaign_id, current_user)

