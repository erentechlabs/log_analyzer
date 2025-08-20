# Log Analyzer and Alerting System
A simple log analysis and alerting system built with:
- FastAPI for a small REST API to fetch logs and alerts
- SQLAlchemy with SQLite for storage
- A lightweight analyzer that detects SSH brute-force attempts from log files
- Optional email notifications for generated alerts

## Features
- Parse SSH failed login attempts from a log file (e.g., auth.log).
- Store parsed log entries in a SQLite database.
- Detect brute-force attempts within a time window and create alerts.
- REST API endpoints to list logs and alerts.
- Optional email notifications on new alerts.

## Project Structure
``` 
project-root/
├─ app/
│  ├─ main.py               # FastAPI application (API)
│  ├─ database.py           # DB engine, SessionLocal, Base
│  ├─ models.py             # SQLAlchemy models (LogEntry, Alert)
│  ├─ crud.py               # Database CRUD operations
│  └─ services/
│     ├─ log_parser.py      # SSH log line parser
│     ├─ analysis_engine.py # Brute-force detection
│     └─ notification.py    # Email notifications
├─ logs/
│  └─ auth.log              # Input log file(s)
└─ run_analyzer.py          # Batch analyzer runner
```
## Requirements
- Python 3.13+
- Virtual environment (recommended)
- Packages:
    - fastapi
    - sqlalchemy
    - uvicorn (for running the API)
    - requests (optional, not required for core functionality)

If you don’t have , you’ll need to install it to serve the FastAPI app. `uvicorn`
## Setup
1. Create and activate a virtual environment:
``` bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```
1. Install dependencies:
``` bash
pip install fastapi sqlalchemy uvicorn
```
1. Ensure the `logs` directory exists and place your inside: `auth.log`
``` bash
mkdir -p logs
# Copy your /var/log/auth.log or a sample log file here as logs/auth.log
```
The database (SQLite file) is created automatically on first run at . `./sql_app.db`
## Configuration (Email Notifications)
Email notifications are optional. If you want to enable them, set environment variables:
- SENDER_EMAIL
- RECEIVER_EMAIL
- EMAIL_PASSWORD

Example:
``` bash
# Linux/macOS
export SENDER_EMAIL="your@gmail.com"
export RECEIVER_EMAIL="dest@example.com"
export EMAIL_PASSWORD="app-specific-password"

# Windows (PowerShell)
$env:SENDER_EMAIL="your@gmail.com"
$env:RECEIVER_EMAIL="dest@example.com"
$env:EMAIL_PASSWORD="app-specific-password"
```
Then, in , you can enable sending emails by uncommenting the line: `run_analyzer.py`
``` python
# notification.send_email_alert(alert)
```
Note: For Gmail, you may need an App Password and to have 2FA enabled.
## Running
### 1) Start the API
From the project root:
``` bash
uvicorn app.main:app --reload
```
- The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Alternatively (if you prefer running as a module):
``` bash
python -m uvicorn app.main:app --reload
```
### 2) Run the Analyzer
In a separate terminal (with the virtual environment activated):
``` bash
python run_analyzer.py
```
This will:
- Parse each line in `logs/auth.log`
- Save parsed entries to the database
- Run brute-force detection (10 failed logins within 5 minutes)
- Create alerts as needed
- Optionally send an email for each new alert if enabled

## API Endpoints
- GET `/`
    - Returns a welcome message.

- GET `/logs/`
    - Query parameters: `skip` (default 0), `limit` (default 100)
    - Returns stored log entries.

- GET `/alerts/`
    - Query parameters: `skip` (default 0), `limit` (default 100)
    - Returns alerts (most recent first).

Example using curl:
``` bash
curl "http://127.0.0.1:8000/logs/?skip=0&limit=10"
curl "http://127.0.0.1:8000/alerts/?skip=0&limit=10"
```
## How It Works
- `log_parser.parse_ssh_log(line)` parses lines with “Failed password for … from …” patterns and returns a dict with:
    - type = "ssh_failed_login"
    - timestamp, username, ip_address, raw_log

- `crud.create_log_entry` saves each parsed log to the DB.
- `analysis_engine.analyze_for_brute_force` checks recent failed attempts by IP and raises an alert if the threshold is exceeded.
- `crud.create_alert` records alerts in the DB.
- `notification.send_email_alert` can notify via email.

## Troubleshooting
- ImportError: attempted relative import with no known parent package
Run the API with uvicorn as shown above, or ensure you run modules from the project root so Python recognizes the `app` package.
- Database file not created or permission errors
Ensure you have write permissions in the project directory for SQLite to create . `sql_app.db`
- No alerts created
Ensure your contains lines that match the parser pattern (SSH failed login lines). `logs/auth.log`
- Email not sent
Verify env vars and email provider settings. For Gmail, use an App Password.

## Security Notes
- Do not commit real credentials to version control.
- Consider rotating and securing App Passwords.
- SQLite is fine for local or small setups; for production, consider PostgreSQL and proper migrations.
