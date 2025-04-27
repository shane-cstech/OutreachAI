from fastapi import FastAPI
from app.api.endpoints import (
    company, proposal, campaign, campaign_lead, email, user, resend_webhook, llm, csv_import, email_send, analytics
)

app = FastAPI()

app.include_router(company.router, prefix="/companies", tags=["companies"])
app.include_router(proposal.router, prefix="/proposals", tags=["proposals"])
app.include_router(campaign.router, prefix="/campaigns", tags=["campaigns"])
app.include_router(campaign_lead.router, prefix="/campaign-leads", tags=["campaign-leads"])
app.include_router(email.router, prefix="/emails", tags=["emails"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(resend_webhook.router, prefix="/resend", tags=["resend"])
app.include_router(llm.router, prefix="/llm", tags=["llm"])
app.include_router(csv_import.router, prefix="/csv", tags=["csv"])
app.include_router(email_send.router, prefix="/email-send", tags=["email-send"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
