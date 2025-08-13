# Stock-Price-Alerting-System
# 📈 Stock Price Alerting System

## 📌 Project Overview
The Stock Price Alerting System allows users to monitor selected stock prices and get notified when certain conditions are met — without using paid APIs or tools.

### ✨ Key Features
- Fetch live prices for 10 predefined companies from a free stock API
- Support for **threshold** and **duration** alerts
- Email and console notifications (mailtrap)
- JWT-based authentication
- Scheduled background tasks for price checks
- AWS Free Tier deployment

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
[ Free Stock API ] → [ Django Backend ] → [ Scheduler ] → [ Alert Logic ] → [ Email/Console Notifications ]
                           ↑
                        [ PostgreSQL DB ]

---

## 📡 API Endpoints

Below is a quick reference to the available API endpoints in the Stock Price Alerting System.  
For detailed request/response examples, parameters, and use cases, please refer to the full documentation in [`API_DOCS.md`](API_DOCS.md).

| Method  | Endpoint                      | Description                               | Auth Required |
|---------|-------------------------------|-------------------------------------------|---------------|
| **POST**| `/api/register/`              | Register a new user                       | ❌            |
| **POST**| `/api/token/`                 | Login and obtain JWT token                | ❌            |
| **GET** | `/api/userinfo/`              | Retrieve current user information         | ✅            |
| **PUT** | `/api/userinfo/update/`       | Update user information                   | ✅            |
| **POST**| `/api/forgot_password/`       | Request password reset                    | ❌            |
| **POST**| `/api/reset_password/<token>/`| Reset password using the provided token   | ❌            |
| **POST**| `/api/logout/`                | Logout the current user                   | ✅            |
| **GET** | `/api/stocks/`                | List Stocks                               | ❌            |
| **GET** | `/api/stocks/<str:symbol>/`   | Stocks details                            | ❌            |
| **GET** | `/api/stocks/`                | List Stocks                               | ❌            |
| **GET** | `/api/alerts/`                | List all alerts                           | ✅            |
| **POST**| `/api/alerts/create/`         | Create a new alert                        | ✅            |
| **GET** | `/api/alerts/<alert_id>/`     | Retrieve details of a specific alert      | ✅            |
| **PUT** | `/api/alerts/<int:pk>//`      | Update a specific alert                   | ✅            |
| **DELETE**| `/api/alerts/<int:pk>/`     | Delete a specific alert                   | ✅            |
| **GET** | `/api/alert-history/`         | List all alert history                    | ✅            |
| **GET** | `/api/notification-log/`      | List all notification logs                | ✅            |


> **📖 Full API documentation:** See [`API_DOCS.md`](API_DOCS.md) for complete details, including payload examples, field descriptions, and response formats.
