Here's a structured and detailed `README.md` file based on the information you provided:

```markdown
# OutreachAI Backend – Feature Overview & Usage Guide

## Project Structure

```
server/
  app/
    api/endpoints/      # All API route files (company, campaign, email, etc.)
    core/               # Config and core logic
    crud/               # CRUD utilities for each model
    db/                 # DB session, base class, and init script
    models/             # SQLAlchemy ORM models
    schemas/            # Pydantic schemas for validation
    services/           # Business logic (email, CSV import, analytics, etc.)
    main.py             # FastAPI app entrypoint
  .env                  # Environment variables
  requirements.txt      # Python dependencies
  README.md             # This file!
```

## Features & How They Work

### 1. CRUD API for All Main Models

**Models**: Company, Campaign, Proposal, CampaignLead, Email, User  
**Endpoints**: `/companies`, `/campaigns`, `/proposals`, `/campaign-leads`, `/emails`, `/users`  
**Operations**: Create, Read, Update, Delete (standard REST)

**How it works**:  
Each endpoint uses Pydantic schemas for validation and SQLAlchemy for DB operations.

**Example**:
- `POST /companies/` to create a company
- `GET /companies/` to list companies
- `PUT /companies/{id}` to update a company
- `DELETE /companies/{id}` to delete a company

---

### 2. CSV Import for Leads

**Endpoint**: `POST /csv/import-leads/`  

**How it works**:  
Upload a CSV file with lead/company data. The service parses and validates each row. Valid leads are inserted into the companies table. A summary of processed, successful, failed, and errors is returned.

**Test**:  
Use Swagger UI (`/docs`) or Postman to upload a CSV file.

---

### 3. Email Sending (SMTP, Background Task)

**Endpoint**: `POST /email-send/send/`

**How it works**:  
Accepts email details (subject, body, recipient, campaign_id, company_id) and sends the email using Gmail SMTP in a FastAPI background task (non-blocking). The sent email is saved in the `emails` table with the status set to `sent`.

**Test**:  
Use Swagger UI or Postman to send a test email.  
Check your Gmail “Sent” folder and the `emails` table in the DB.

---

### 4. Resend Webhook for Email Status Tracking

**Endpoint**: `POST /resend/webhook`

**How it works**:  
Resend calls this endpoint with email event data (sent, delivered, opened, replied). The service updates the corresponding Email record in the DB (status, opened_at, replied_at).

**Test**:  
Use a tool like Postman to POST a sample event payload to `/resend/webhook`.

**Example Payload**:
```json
{
  "type": "opened",
  "data": {
    "tracking_id": "abc123"
  }
}
```

Check the `emails` table for updated status/timestamps.

---

### 5. Analytics Endpoint

**Endpoint**: `GET /analytics/email-status-counts/`

**How it works**:  
Returns a count of emails by status (sent, received, replied). You can optionally filter by campaign.

**Test**:  
Visit `/analytics/email-status-counts/` in Swagger UI or Postman.

---

### 6. LLM (GenAI) Endpoints

**Endpoints**:
- `POST /llm/generate-email/` – Generate a personalized email draft using AI.
- `POST /llm/generate-report/` – Generate a summary/report for a lead’s conversation.

**How it works**:  
Accepts lead/campaign data and/or conversation history and returns a stub response (replace with your GenAI logic).

**Test**:  
Use Swagger UI or Postman to POST sample data and get a generated response.

---

## How to Test the System

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up your `.env` file with your local DB and SMTP credentials.

### 3. Create the Database (if not exists) using your DB creation script.
```bash
python -m app.db.init_db
```

### 4. Run the FastAPI App
```bash
uvicorn app.main:app --reload
```

### 5. Open Swagger UI
Go to [http://localhost:8000/docs](http://localhost:8000/docs). All endpoints are documented and testable here.

### 6. Test Each Feature
- **CRUD**: Use the `/companies`, `/campaigns`, etc. endpoints.
- **CSV Import**: Use `/csv/import-leads/` to upload a CSV.
- **Email Send**: Use `/email-send/send/` to send a test email.
- **Resend Webhook**: POST to `/resend/webhook` with a sample event.
- **Analytics**: GET `/analytics/email-status-counts/`
- **LLM**: POST to `/llm/generate-email/` or `/llm/generate-report/`

---

## Example `.env` File

```ini
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=outreachai

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_gmail_app_password

RESEND_WEBHOOK_SECRET=your_resend_webhook_secret
```

---

## Notes for Developers

- All endpoints are modular and can be extended.
- For production, consider adding authentication, logging, and webhook security.
- LLM endpoints are stubs—connect to your GenAI logic as needed.
- For Resend, configure your webhook URL in the Resend dashboard to point to `/resend/webhook`.
```

This `README.md` provides a clear structure with explanations for the project, its features, and how to set up and test the system. Let me know if you'd like any changes!