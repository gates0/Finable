from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from models.campaign import Campaign
from schemas.campaign import CampaignCreate, CampaignUpdate
from services.upload import save_uploaded_file
from datetime import datetime, date
import os

def create_campaign(
    db: Session,
    current_user,
    campaign_data: CampaignCreate,
    cover_photo: UploadFile
):
    # Save image
    photo_path = save_uploaded_file(cover_photo)

    # Create campaign record
    new_campaign = Campaign(
        user_id=current_user.id,
        country="Nigeria",
        cover_photo=photo_path,
        **campaign_data.dict()  # unpack all fields from schema
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

def get_all_campaigns(db: Session):
    campaigns = db.query(Campaign).all()
    return campaigns

def update_campaign(
    db: Session,
    campaign_id: int,
    user_id: str,
    data: CampaignUpdate,
    cover_photo: UploadFile = None
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if campaign.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this campaign")

    for field, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(campaign, field, value)

    if cover_photo:
        if campaign.cover_photo and os.path.exists(campaign.cover_photo):
            os.remove(campaign.cover_photo)
        photo_path = save_uploaded_file(cover_photo)
        campaign.cover_photo = photo_path

    db.commit()
    db.refresh(campaign)
    return campaign

def delete_campaign(db: Session, campaign_id: int, current_user):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Optional ownership check
    if current_user and campaign.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this campaign"
        )

    db.delete(campaign)
    db.commit()

    return {"message": "Campaign deleted successfully"}
