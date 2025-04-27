from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ProposalBase(BaseModel):
    company_id: uuid.UUID
    file_url: Optional[str] = None
    created_at: Optional[datetime] = None

class ProposalCreate(ProposalBase):
    pass

class ProposalUpdate(ProposalBase):
    pass

class ProposalInDBBase(ProposalBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class Proposal(ProposalInDBBase):
    pass