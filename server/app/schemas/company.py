from typing import List, Optional
from pydantic import BaseModel, EmailStr
import uuid

class CompanyBase(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    lead_stage: Optional[str] = None
    interests: Optional[List[str]] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class CompanyCreate(CompanyBase):
    company_name: str
    email: EmailStr

class CompanyUpdate(CompanyBase):
    pass

class CompanyInDBBase(CompanyBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class Company(CompanyInDBBase):
    pass