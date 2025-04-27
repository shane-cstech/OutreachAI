from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.email import Email, EmailCreate, EmailUpdate
from app.crud.email import (
    get_email, get_emails, create_email, update_email, delete_email
)
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Email])
def read_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_emails(db, skip=skip, limit=limit)

@router.get("/{email_id}", response_model=Email)
def read_email(email_id: str, db: Session = Depends(get_db)):
    db_email = get_email(db, email_id)
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    return db_email

@router.post("/", response_model=Email)
def create_new_email(email: EmailCreate, db: Session = Depends(get_db)):
    return create_email(db, email)

@router.put("/{email_id}", response_model=Email)
def update_existing_email(email_id: str, updates: EmailUpdate, db: Session = Depends(get_db)):
    db_email = get_email(db, email_id)
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    return update_email(db, db_email, updates)

@router.delete("/{email_id}")
def delete_existing_email(email_id: str, db: Session = Depends(get_db)):
    db_email = get_email(db, email_id)
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    delete_email(db, db_email)
    return {"ok": True}