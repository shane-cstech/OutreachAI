from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
import enum

class CampaignStatusEnum(str, enum.Enum):
    sent = "sent"
    received = "received"
    replied = "replied"

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    name = Column(String)
    description = Column(Text)
    status = Column(Enum(CampaignStatusEnum), default=CampaignStatusEnum.sent)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    leads = relationship("CampaignLead", back_populates="campaign")
    emails = relationship("Email", back_populates="campaign")