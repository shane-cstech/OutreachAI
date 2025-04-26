from sqlalchemy import (
    create_engine, Column, String, Text, Integer, ForeignKey, Table, DateTime, UUID, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine=create_engine(DATABASE_URL)
Base = declarative_base()

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


class Proposal(Base):
    __tablename__ = 'proposals'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    file_url = Column(String)
    created_at = Column(DateTime)
    slide_count = Column(Integer)

    company = relationship("Company", back_populates="proposals")


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    name = Column(String)
    description = Column(Text)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


    leads = relationship("CampaignLead", back_populates="campaign")
    emails = relationship("Email", back_populates="campaign")


class CampaignLead(Base):
    __tablename__ = 'campaign_leads'

    campaign_id = Column(PGUUID(as_uuid=True), ForeignKey('campaigns.id'), primary_key=True)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), primary_key=True)
    added_at = Column(DateTime)


    campaign = relationship("Campaign", back_populates="leads")
    company = relationship("Company", back_populates="campaign_leads")


class Email(Base):
    __tablename__ = 'emails'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(PGUUID(as_uuid=True), ForeignKey('campaigns.id'), nullable=False)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    subject = Column(Text)
    body = Column(Text)
    status = Column(String)
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    replied_at = Column(DateTime)
    tracking_id = Column(String)


    campaign = relationship("Campaign", back_populates="emails")
    company = relationship("Company", back_populates="emails")

def createTableNotExist():
    Base.metadata.create_all(engine)

if __name__=='__main__':
    createTableNotExist()