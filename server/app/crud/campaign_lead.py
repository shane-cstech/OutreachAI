from sqlalchemy.orm import Session
from app.models.campaign_lead import CampaignLead
from app.schemas.campaign_lead import CampaignLeadCreate, CampaignLeadUpdate
from typing import List, Optional
import uuid

def get_campaign_lead(db: Session, campaign_id: uuid.UUID, company_id: uuid.UUID) -> Optional[CampaignLead]:
    return db.query(CampaignLead).filter(
        CampaignLead.campaign_id == campaign_id,
        CampaignLead.company_id == company_id
    ).first()

def get_campaign_leads(db: Session, skip: int = 0, limit: int = 100) -> List[CampaignLead]:
    return db.query(CampaignLead).offset(skip).limit(limit).all()

def create_campaign_lead(db: Session, campaign_lead: CampaignLeadCreate) -> CampaignLead:
    db_campaign_lead = CampaignLead(**campaign_lead.dict())
    db.add(db_campaign_lead)
    db.commit()
    db.refresh(db_campaign_lead)
    return db_campaign_lead

def update_campaign_lead(db: Session, db_campaign_lead: CampaignLead, updates: CampaignLeadUpdate) -> CampaignLead:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_campaign_lead, field, value)
    db.commit()
    db.refresh(db_campaign_lead)
    return db_campaign_lead

def delete_campaign_lead(db: Session, db_campaign_lead: CampaignLead):
    db.delete(db_campaign_lead)
    db.commit()