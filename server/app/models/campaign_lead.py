from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class CampaignLead(Base):
    __tablename__ = 'campaign_leads'

    campaign_id = Column(PGUUID(as_uuid=True), ForeignKey('campaigns.id'), primary_key=True)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), primary_key=True)
    added_at = Column(DateTime)

    campaign = relationship("Campaign", back_populates="leads")
    company = relationship("Company", back_populates="campaign_leads")