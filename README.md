# Gym CRM Backend

This is the backend for the Gym CRM project, built with Django and Django REST Framework. It is designed to serve both a React web application and a React Native mobile application.

## 🚀 Setup Instructions

### 1. Python Version
Ensure you are using **Python 3.14.4** as intended for this project.

### 2. Virtual Environment Setup
Create and activate a virtual environment in the root directory:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Dependency Installation
Install the necessary Python packages:
```bash
pip install -r requirements.txt
```

### 4. .env Configuration
The project is configured to enforce 12-factor principles. You must create a `.env` file in the root directory (alongside `manage.py`). 
**Never commit this file to Git.**

```env
# .env
SECRET_KEY=your-secure-secret-key
DEBUG=True
CORS_ALLOW_ALL_ORIGINS=True

# Database Configuration (PostgreSQL)
DB_NAME=gym_crm_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 5. PostgreSQL Setup
This project **requires** PostgreSQL. The fallback to SQLite has been completely removed to ensure development matches production behavior.
- Ensure PostgreSQL is installed and running on your machine.
- Create a database matching the `DB_NAME` in your `.env` file.
- Verify that the `DB_USER` and `DB_PASSWORD` can connect to `DB_HOST` on `DB_PORT`.

### 6. Django Checks
Validate your environment before applying migrations:
```bash
python manage.py check
```

### 7. Migrations
Apply the database schemas to PostgreSQL:
```bash
python manage.py migrate
```

### 8. Creating a Superuser
Once the database is migrated, create an admin user:
```bash
python manage.py createsuperuser
```

### 9. Running the Development Server
```bash
python manage.py runserver
```

---

## 🏗️ Architecture Overview

The backend uses a modular monolithic architecture, providing clean boundaries between domains.

### Current Project Structure
```
apps/
├── organizations/
│   ├── Organization  # Core tenant model
│   └── Branch        # Physical locations belonging to an Organization
│
└── users/
    └── User          # Custom auth model with email-based login
```

### Multi-Tenant Architecture & Data Isolation
- **Organization & Branch Scope:** Every user belongs to an `Organization` and a `Branch`.
- **API Security Rule:** Future APIs will derive the organization/branch scope from the authenticated user and server-side permissions. The API will **never** trust `organization_id` or `branch_id` parameters sent from the frontend to determine access. Data isolation is enforced strictly on the backend.
- **Unique Constraints:** A composite database constraint ensures that `Branch` codes are unique *per organization*, rather than globally.

### Future Modules:
- `members`: Gym Member profiles.
- `memberships`: Member subscription plans.
- `attendance`: Manual and device-based member check-ins.
- `payments`: Financial transaction tracking.
- `trainers` & `workouts`: Staff and plan management.
- `notifications`: Reminders.
- `reports`: Analytics.
- `audit_logs`: Tracking crucial system actions.

## 🔒 Security
- **No SQLite Fallback:** PostgreSQL is strictly enforced to prevent accidental SQLite deployment.
- **No Hardcoded Secrets:** `SECRET_KEY`, database credentials, and CORS settings are exclusively read from environment variables.
- **JWT Authentication:** Secure stateless authentication for web and mobile clients.