from app.db.session import engine
from app.models import base, user, company, campaign, email, proposal, campaign_lead

def init_db():
    base.Base.metadata.create_all(bind=engine)