import re
from email_validator import validate_email, EmailNotValidError
from typing import Dict, List, Tuple

def validate_lead_data(data: Dict) -> Tuple[bool, List[str]]:
    errors = []
    
    # Required fields check
    required_fields = ['first_name', 'last_name', 'email', 'company_name']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Email validation
    if data.get('email'):
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            errors.append("Invalid email format")
    
    # Name validation (basic)
    if data.get('first_name') and len(data['first_name'].strip()) < 1:
        errors.append("First name cannot be empty")
    if data.get('last_name') and len(data['last_name'].strip()) < 1:
        errors.append("Last name cannot be empty")
    
    return len(errors) == 0, errors