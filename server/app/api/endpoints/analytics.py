from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.analytics_service import get_email_status_counts
from app.db.session import SessionLocal
from typing import Optional
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/email-status-counts/")
def email_status_counts(
    campaign_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db)
):
    return get_email_status_counts(db, campaign_id=campaign_id)