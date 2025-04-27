from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from app.services.resend_service import handle_resend_event
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def resend_webhook(request: Request, db: Session = Depends(get_db)):
    event = await request.json()
    handle_resend_event(event, db)
    return {"ok": True}