from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LLMEmailRequest(BaseModel):
    lead_data: dict
    campaign_data: Optional[dict] = None
    prompt: Optional[str] = None

@router.post("/generate-email/")
async def generate_email(request: LLMEmailRequest):
    """
    Generate a personalized email draft using LLM.
    This is a stub. Replace with your actual GenAI integration.
    """
    # Example: Call your GenAI service here
    # generated_email = your_llm_service.generate_email(request.lead_data, request.campaign_data, request.prompt)
    generated_email = f"Hi {request.lead_data.get('first_name', 'there')},\n\nThis is a personalized email draft generated by AI."
    return {"generated_email": generated_email}

class LLMReportRequest(BaseModel):
    conversation: list  # List of dicts/messages
    lead_data: Optional[dict] = None

@router.post("/generate-report/")
async def generate_report(request: LLMReportRequest):
    """
    Generate a summary/report for a lead's conversation using LLM.
    This is a stub. Replace with your actual GenAI integration.
    """
    # Example: Call your GenAI service here
    # report = your_llm_service.generate_report(request.conversation, request.lead_data)
    report = f"Report for {request.lead_data.get('first_name', 'Lead')}: This is a summary of the conversation."
    return {"report": report}