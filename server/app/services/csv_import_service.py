import pandas as pd
from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate
from typing import Dict, Any
from email_validator import validate_email, EmailNotValidError

REQUIRED_FIELDS = ["company_name", "email"]

def validate_lead(row: dict) -> (bool, str):
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            return False, f"Missing required field: {field}"
    try:
        validate_email(row["email"])
    except EmailNotValidError:
        return False, "Invalid email format"
    return True, ""

def import_leads_from_csv(file_path: str, db: Session) -> Dict[str, Any]:
    stats = {"processed": 0, "success": 0, "failed": 0, "errors": []}
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        stats["errors"].append(f"Failed to read CSV: {e}")
        return stats

    for idx, row in df.iterrows():
        stats["processed"] += 1
        lead_data = row.to_dict()
        is_valid, error = validate_lead(lead_data)
        if not is_valid:
            stats["failed"] += 1
            stats["errors"].append(f"Row {idx+1}: {error}")
            continue
        try:
            company_in = CompanyCreate(**lead_data)
            company = Company(**company_in.dict())
            db.add(company)
            db.commit()
            db.refresh(company)
            stats["success"] += 1
        except Exception as e:
            db.rollback()
            stats["failed"] += 1
            stats["errors"].append(f"Row {idx+1}: DB error: {e}")
    return stats