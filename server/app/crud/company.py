from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from typing import List, Optional
import uuid

def get_company(db: Session, company_id: uuid.UUID) -> Optional[Company]:
    return db.query(Company).filter(Company.id == company_id).first()

def get_company_by_email(db: Session, email: str) -> Optional[Company]:
    return db.query(Company).filter(Company.email == email).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate) -> Company:
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, db_company: Company, updates: CompanyUpdate) -> Company:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_company, field, value)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, db_company: Company):
    db.delete(db_company)
    db.commit()