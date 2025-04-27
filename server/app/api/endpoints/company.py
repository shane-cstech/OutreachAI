from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.company import Company, CompanyCreate, CompanyUpdate
from app.crud.company import (
    get_company, get_companies, create_company, update_company, delete_company
)
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_companies(db, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=Company)
def read_company(company_id: str, db: Session = Depends(get_db)):
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.post("/", response_model=Company)
def create_new_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return create_company(db, company)

@router.put("/{company_id}", response_model=Company)
def update_existing_company(company_id: str, updates: CompanyUpdate, db: Session = Depends(get_db)):
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return update_company(db, db_company, updates)

@router.delete("/{company_id}")
def delete_existing_company(company_id: str, db: Session = Depends(get_db)):
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    delete_company(db, db_company)
    return {"ok": True}