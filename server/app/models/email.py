from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
import enum

class EmailStatusEnum(str, enum.Enum):
    sent = "sent"
    received = "received"
    replied = "replied"

class Email(Base):
    __tablename__ = 'emails'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(PGUUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=False)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    subject = Column(Text)
    body = Column(Text)
    status = Column(Enum(EmailStatusEnum), default=EmailStatusEnum.sent)
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    replied_at = Column(DateTime)
    tracking_id = Column(String)

    campaign = relationship("Campaign", back_populates="emails")
    company = relationship("Company", back_populates="emails")