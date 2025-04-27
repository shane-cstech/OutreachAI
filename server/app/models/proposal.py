from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class Proposal(Base):
    __tablename__ = 'proposals'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(PGUUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    file_url = Column(String)
    created_at = Column(DateTime)

    company = relationship("Company", back_populates="proposals")