import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/leads_db')
CHUNK_SIZE = 1000  # Number of records to process at once for CSV
REQUIRED_COLUMNS = [
    'first_name', 'last_name', 'company_name', 'email',
    'industry', 'lead_stage', 'interests', 'location'
]