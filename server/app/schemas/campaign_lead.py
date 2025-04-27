from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class CampaignLeadBase(BaseModel):
    campaign_id: uuid.UUID
    company_id: uuid.UUID
    added_at: Optional[datetime] = None

class CampaignLeadCreate(CampaignLeadBase):
    pass

class CampaignLeadUpdate(CampaignLeadBase):
    pass

class CampaignLeadInDBBase(CampaignLeadBase):
    class Config:
        orm_mode = True

class CampaignLead(CampaignLeadInDBBase):
    pass