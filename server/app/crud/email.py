from sqlalchemy.orm import Session
from app.models.email import Email
from app.schemas.email import EmailCreate, EmailUpdate
from typing import List, Optional
import uuid

def get_email(db: Session, email_id: uuid.UUID) -> Optional[Email]:
    return db.query(Email).filter(Email.id == email_id).first()

def get_emails(db: Session, skip: int = 0, limit: int = 100) -> List[Email]:
    return db.query(Email).offset(skip).limit(limit).all()

def create_email(db: Session, email: EmailCreate) -> Email:
    db_email = Email(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def update_email(db: Session, db_email: Email, updates: EmailUpdate) -> Email:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_email, field, value)
    db.commit()
    db.refresh(db_email)
    return db_email

def delete_email(db: Session, db_email: Email):
    db.delete(db_email)
    db.commit()