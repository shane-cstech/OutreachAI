from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from app.models.email import EmailStatusEnum, EmailRoleEnum, EmailResponseTypeEnum

class EmailBase(BaseModel):
    campaign_id: uuid.UUID
    company_id: uuid.UUID
    subject: Optional[str] = None
    body: Optional[str] = None
    status: Optional[EmailStatusEnum] = None
    sent_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    tracking_id: Optional[str] = None
    role: Optional[EmailRoleEnum] = None
    response_type: Optional[EmailResponseTypeEnum] = None

class EmailCreate(EmailBase):
    subject: str
    body: str

class EmailUpdate(EmailBase):
    pass

class EmailInDBBase(EmailBase):
    id: uuid.UUID

    class Config:
        from_attributes = True  # For Pydantic v2

class Email(EmailInDBBase):
    pass