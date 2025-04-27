from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from app.models.campaign import CampaignStatusEnum

class CampaignBase(BaseModel):
    company_id: uuid.UUID
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatusEnum] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    name: str

class CampaignUpdate(CampaignBase):
    pass

class CampaignInDBBase(CampaignBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class Campaign(CampaignInDBBase):
    pass