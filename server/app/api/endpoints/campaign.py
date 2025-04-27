from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate
from app.crud.campaign import (
    get_campaign, get_campaigns, create_campaign, update_campaign, delete_campaign
)
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Campaign])
def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_campaigns(db, skip=skip, limit=limit)

@router.get("/{campaign_id}", response_model=Campaign)
def read_campaign(campaign_id: str, db: Session = Depends(get_db)):
    db_campaign = get_campaign(db, campaign_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.post("/", response_model=Campaign)
def create_new_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    return create_campaign(db, campaign)

@router.put("/{campaign_id}", response_model=Campaign)
def update_existing_campaign(campaign_id: str, updates: CampaignUpdate, db: Session = Depends(get_db)):
    db_campaign = get_campaign(db, campaign_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return update_campaign(db, db_campaign, updates)

@router.delete("/{campaign_id}")
def delete_existing_campaign(campaign_id: str, db: Session = Depends(get_db)):
    db_campaign = get_campaign(db, campaign_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    delete_campaign(db, db_campaign)
    return {"ok": True}