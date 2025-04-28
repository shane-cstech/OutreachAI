from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.services.email_service import send_email_smtp
from app.db.session import SessionLocal
from app.schemas.email import EmailCreate
from typing import Optional
from app.schemas.email import Email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send/", response_model=Optional[Email])
def send_email_endpoint(
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        background_tasks.add_task(
            send_email_smtp,
            subject=email.subject,
            body=email.body,
            to_email=email.to_email,  # Add this field to your EmailCreate schema!
            db=db,
            campaign_id=email.campaign_id,
            company_id=email.company_id,
            tracking_id=email.tracking_id,
        )
        return {"message": "Email is being sent in the background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))