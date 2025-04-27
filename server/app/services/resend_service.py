from sqlalchemy.orm import Session
from app.models.email import Email, EmailStatusEnum
from datetime import datetime

def handle_resend_event(event: dict, db: Session):
    # Example event: {"type": "delivered", "data": {"tracking_id": "...", ...}}
    event_type = event.get("type")
    data = event.get("data", {})
    tracking_id = data.get("tracking_id")
    if not tracking_id:
        return

    email = db.query(Email).filter(Email.tracking_id == tracking_id).first()
    if not email:
        return

    if event_type == "delivered":
        email.status = EmailStatusEnum.received
    elif event_type == "opened":
        email.opened_at = datetime.utcnow()
    elif event_type == "replied":
        email.status = EmailStatusEnum.replied
        email.replied_at = datetime.utcnow()
    elif event_type == "sent":
        email.status = EmailStatusEnum.sent

    db.commit()