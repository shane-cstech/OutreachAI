from sqlalchemy.orm import Session
from app.models.email import Email, EmailStatusEnum

def get_email_status_counts(db: Session, campaign_id=None):
    query = db.query(Email.status, db.func.count(Email.id)).group_by(Email.status)
    if campaign_id:
        query = query.filter(Email.campaign_id == campaign_id)
    results = query.all()
    # Convert to dict: {status: count}
    return {status.value: count for status, count in results}