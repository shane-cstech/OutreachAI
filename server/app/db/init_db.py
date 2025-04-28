from app.db.session import engine
from app.db.base_class import Base
from app.models import company, proposal, campaign, campaign_lead, email, user

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("All tables created!")