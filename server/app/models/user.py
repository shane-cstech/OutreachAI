from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid
from app.db.base_class import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    # Add more fields as needed