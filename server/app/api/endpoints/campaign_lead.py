from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.campaign_lead import CampaignLead, CampaignLeadCreate, CampaignLeadUpdate
from app.crud.campaign_lead import (
    get_campaign_lead, get_campaign_leads, create_campaign_lead, update_campaign_lead, delete_campaign_lead
)
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CampaignLead])
def read_campaign_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_campaign_leads(db, skip=skip, limit=limit)

@router.get("/{campaign_id}/{company_id}", response_model=CampaignLead)
def read_campaign_lead(campaign_id: str, company_id: str, db: Session = Depends(get_db)):
    db_campaign_lead = get_campaign_lead(db, campaign_id, company_id)
    if not db_campaign_lead:
        raise HTTPException(status_code=404, detail="CampaignLead not found")
    return db_campaign_lead

@router.post("/", response_model=CampaignLead)
def create_new_campaign_lead(campaign_lead: CampaignLeadCreate, db: Session = Depends(get_db)):
    return create_campaign_lead(db, campaign_lead)

@router.put("/{campaign_id}/{company_id}", response_model=CampaignLead)
def update_existing_campaign_lead(campaign_id: str, company_id: str, updates: CampaignLeadUpdate, db: Session = Depends(get_db)):
    db_campaign_lead = get_campaign_lead(db, campaign_id, company_id)
    if not db_campaign_lead:
        raise HTTPException(status_code=404, detail="CampaignLead not found")
    return update_campaign_lead(db, db_campaign_lead, updates)

@router.delete("/{campaign_id}/{company_id}")
def delete_existing_campaign_lead(campaign_id: str, company_id: str, db: Session = Depends(get_db)):
    db_campaign_lead = get_campaign_lead(db, campaign_id, company_id)
    if not db_campaign_lead:
        raise HTTPException(status_code=404, detail="CampaignLead not found")
    delete_campaign_lead(db, db_campaign_lead)
    return {"ok": True}