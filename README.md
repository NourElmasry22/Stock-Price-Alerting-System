# 📈 Stock Price Alerting System

## 📌 Project Overview
The **Stock Price Alerting System** allows users to monitor selected stock prices and get notified when certain conditions are met — without using paid APIs or tools.

### ✨ Key Features
- Fetch live prices for **10 predefined companies** from a free stock API.
- Support for **threshold** and **duration** alerts.
- Email and console notifications (via Mailtrap).
- JWT-based authentication.
- Scheduled background tasks for price checks.
- Complete REST API with pagination and filtering.
- **Alert Management**: Create, read, update, delete alerts.
- **Stock Management**: Browse stocks, view price history.
- **Notification Logs**: Track all sent notifications.
- **Alert History**: Complete history of triggered alerts.
- **Data Cleanup**: Automated cleanup of old data.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Authentication:** JWT
- **Scheduling:** APScheduler
- **API Source:** Twelve Data
- **Deployment:** AWS Free Tier

---

## 🗂️ System Architecture
```plaintext
[ Free Stock API (Twelve) ] → [ Django Backend ] → [ Scheduler ] → [ Alert Logic ] → [ Email/Console Notifications ]
                                   ↑
                           [ PostgreSQL DB ]
```


## 🗂️ Components

### Django API Server
- Provides RESTful API endpoints for users and alerts.
- Handles JWT authentication.
- Manages CRUD operations for alerts, stocks, users, and notifications.

### APScheduler
- Periodically fetches stock prices from the Twelve Data API.
- Checks alert conditions every minute.
- Triggers email and console notifications when conditions are met.
- Performs daily cleanup of old records.

### Database
- PostgreSQL for production; SQLite for local development.
- Stores user data, alert definitions, stock history, notification logs, and alert history.

### External APIs
- Free stock price provider (Twelve Data).
- Supplies real-time stock data for processing by the system.

---

## 🔄 Data Flow

1. **Stock Data**
   - APScheduler fetches stock prices every 5 minutes from the API.
2. **Alert Checking**
   - APScheduler evaluates all alert conditions every minute.
3. **Notifications**
   - Emails or console messages are sent when an alert is triggered.
4. **Cleanup**
   - Old alerts, logs, and stock data are automatically removed daily.

---

## 🔧 Configuration

### Predefined Stocks
By default, the system monitors:
- **AAPL** (Apple Inc.)
- **GOOGL** (Alphabet Inc.)
- **MSFT** (Microsoft Corporation)
- **AMZN** (Amazon.com Inc.)
- **TSLA** (Tesla Inc.)
- **META** (Meta Platforms Inc.)
- **NVDA** (NVIDIA Corporation)
- **NFLX** (Netflix Inc.)
- **CRM** (Salesforce Inc.)
- **ADBE** (Adobe Inc.)

### Alert Types
- **Threshold Alerts**: Trigger immediately when the condition is met.
- **Duration Alerts**: Trigger when the condition persists for a specified time.

### Notification Settings
- Email notifications via SMTP (Gmail recommended).
- Test notifications available for debugging.
- Notification history tracking.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9+
- Django
- PostgreSQL

### 1. Clone and Setup
```bash
git clone <your_repo_url>
cd <project_folder>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

## 2. Environment Configuration
Create a `.env` file in the project root with the following content:

```ini
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password

## 3. Database Setup
```ini
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py init_stocks --fetch-data

## 4. Start Services
```ini
# Terminal 1: Start Django server
python manage.py runserver

# Terminal 2: Start APScheduler job runner
python manage.py runapscheduler

```
---

## 📡 API Endpoints

Below is a quick reference for all available endpoints. For full details, see [`API_DOCS.md`](API_DOCS.md).

| Method    | Endpoint                        | Description                               | Auth Required |
|-----------|---------------------------------|-------------------------------------------|---------------|
| POST      | `/api/register/`                | Register a new user                       | ❌            |
| POST      | `/api/token/`                   | Login and obtain JWT token                | ❌            |
| GET       | `/api/userinfo/`                | Retrieve current user information         | ✅            |
| PUT       | `/api/userinfo/update/`         | Update user information                   | ✅            |
| POST      | `/api/forgot_password/`         | Request password reset                    | ❌            |
| POST      | `/api/reset_password/<token>/`  | Reset password using the provided token   | ❌            |
| POST      | `/api/logout/`                  | Logout the current user                   | ✅            |
| GET       | `/api/stocks/`                  | List all stocks                           | ❌            |
| GET       | `/api/stocks/<str:symbol>/`     | Get stock details for a specific symbol   | ❌            |
| GET       | `/api/alerts/`                  | List all alerts                           | ✅            |
| POST      | `/api/alerts/create/`           | Create a new alert                        | ✅            |
| GET       | `/api/alerts/<alert_id>/`       | Get details of a specific alert           | ✅            |
| PUT       | `/api/alerts/<int:pk>/`         | Update a specific alert                   | ✅            |
| DELETE    | `/api/alerts/<int:pk>/`         | Delete a specific alert                   | ✅            |
| GET       | `/api/alert-history/`           | List all alert history                    | ✅            |
| GET       | `/api/notification-log/`        | List all notification logs                | ✅            |

> **📖 Full API Documentation:** See [`API_DOCS.md`](API_DOCS.md) for detailed request/response examples, payloads, and use cases.
---
