from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    company_name = Column(String(200))
    email = Column(String(200), unique=True)
    industry = Column(String(100))
    lead_stage = Column(String(50))
    interests = Column(Text)
    location = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())