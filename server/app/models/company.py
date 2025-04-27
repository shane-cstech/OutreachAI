from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(Text)
    industry = Column(String)
    website = Column(String)
    description = Column(Text)
    location = Column(String)
    lead_stage = Column(String)
    interests = Column(ARRAY(String))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)

    proposals = relationship("Proposal", back_populates="company")
    campaign_leads = relationship("CampaignLead", back_populates="company")
    emails = relationship("Email", back_populates="company")