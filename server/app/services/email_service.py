import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from app.models.email import Email, EmailStatusEnum
from app.schemas.email import EmailCreate
from app.core.config import settings
from datetime import datetime

def send_email_smtp(
    subject: str,
    body: str,
    to_email: str,
    db: Session,
    campaign_id,
    company_id,
    tracking_id: str = None
):
    # Compose the email
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USERNAME, to_email, msg.as_string())
        # Save to DB as sent
        email_obj = Email(
            campaign_id=campaign_id,
            company_id=company_id,
            subject=subject,
            body=body,
            status=EmailStatusEnum.sent,
            sent_at=datetime.utcnow(),
            tracking_id=tracking_id,
        )
        db.add(email_obj)
        db.commit()
        db.refresh(email_obj)
        return email_obj
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to send email: {e}")