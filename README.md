OutreachAI Backend
A FastAPI backend for GenAI-powered email marketing campaigns, with CSV/CRM lead import, campaign management, email sending/tracking, and analytics.
Project Structure

server/
  app/
    api/
      endpoints/
      ...
    core/
    crud/
    db/
    models/
    schemas/
    services/
    main.py
  .env
  requirements.txt
  README.md

Setup Instructions
1. Clone the Repository
git clone <your-repo-url>
cd OutreachAI/server

2. Set Up Python Environment
Using conda:
conda create -n AIzone python=3.10
conda activate AIzone

Or using venv:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Edit .env in the server/ directory:
POSTGRES_SERVER=localhost
POSTGRES_USER=your_pg_user
POSTGRES_PASSWORD=your_pg_password
POSTGRES_DB=outreachai
POSTGRES_PORT=5432

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_gmail_app_password

RESEND_WEBHOOK_SECRET=your_resend_webhook_secret

5. Create the Database
If not already created:
Use pgAdmin or psql to create a database named outreachai.
6. Run Database Migrations / Create Tables
Option 1: Using SQLAlchemy (dev only):
python -m app.db.init_db

Option 2: Using Alembic (recommended for production):
alembic upgrade head

(Make sure your alembic.ini and env.py are configured for your app!)
7. Start the FastAPI Server
From the server/ directory:
uvicorn app.main:app --reload

The server will be available at http://localhost:8000
Swagger UI docs: http://localhost:8000/docs

Key Features & Endpoints
CRUD APIs
/companies/ — Manage companies/leads
/campaigns/ — Manage campaigns
/emails/ — Manage emails (with role and response_type fields)
/proposals/, /campaign-leads/, /users/ — Other entities
CSV Import
POST /csv/import-leads/
Upload a CSV file to bulk import leads into the companies table.
Email Sending
POST /email-send/send/
Send an email via SMTP (runs as a background task).
Resend Webhook
POST /resend/webhook
Receives email status events (sent, opened, replied) from Resend and updates the DB.
Analytics
GET /analytics/email-status-counts/
Get counts of emails by status (for dashboard pie charts, etc.).
LLM Endpoints
POST /llm/generate-email/ — Generate a personalized email draft using GenAI.
POST /llm/generate-report/ — Generate a summary/report for a lead’s conversation.
How to Test
Open Swagger UI:
http://localhost:8000/docs
Try the endpoints:
Upload a CSV file to /csv/import-leads/
Send a test email via /email-send/send/
Check analytics at /analytics/email-status-counts/
Test LLM endpoints
Check your database:
Use pgAdmin, DBeaver, or psql to view the tables and data.
Troubleshooting
ModuleNotFoundError:
Make sure you are running uvicorn from the server/ directory:
  cd server
  uvicorn app.main:app --reload
  
Missing dependencies:
Install any missing packages with pip install <package> and update requirements.txt.
Database errors:
Ensure your .env matches your local PostgreSQL setup and the DB exists.
CSV import errors:
Make sure your CSV header matches the expected fields exactly.
Development Notes
For development, you can drop and recreate tables as needed.
For production, use Alembic for migrations.
To disable validation for testing, comment out the validation logic in csv_import_service.py.
The emails table now includes role (enum: user, company) and response_type (enum: interested, not_interested, neutral).
Contributing
Fork the repo
Create a feature branch
Commit your changes
Open a pull request
Contact
For questions, contact the backend team or open an issue in the repository.
Happy hacking! 🚀