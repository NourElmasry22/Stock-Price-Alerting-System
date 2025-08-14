# API Documentation

## Base URL
```
http://localhost:8000/api/
```

---

## Authentication

Most endpoints require authentication using a JWT token.

**Public endpoints:**  
- `/signup`
- `/forgot_password`
- `/reset_password/<token>`

**Protected endpoints:**  
- `/current_user`
- `/update_user`
- All `/stocks/*` endpoints
- All `/alerts/*` endpoints

**How to Authenticate:**  
Include your token in the `Authorization` header:
```
Authorization: Bearer <your_token>
```

---

# Stocks API

## 1. List All Stocks

**Endpoint:**  
`GET /stocks/`

**Description:**  
Returns a list of all stocks with their latest price.

**Response:**
```json
{
    "id": 1,
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "exchange": "NASDAQ",
    "sector": "Technology",
    "is_active": true,
    "created_at": "2025-08-12T20:33:02.346493Z",
    "latest_price": {
      "price": "192.45",
      "timestamp": "2025-08-13T14:30:00Z",
      "open_price": "190.00",
      "high_price": "193.00",
      "low_price": "189.50",
      "volume": 1200000
    }
}
```

---

## 2. Get Stock Details by Symbol

**Endpoint:**  
`GET /stocks/{symbol}/`

**Description:**  
Returns details for a specific stock, including its latest price and price history.

**Response:**
```json
{
  "id": 1,
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "exchange": "NASDAQ",
  "sector": "Technology",
  "is_active": true,
  "created_at": "2025-08-12T20:33:02.346493Z",
  "latest_price": {
    "price": "192.45",
    "timestamp": "2025-08-13T14:30:00Z",
    "open_price": "190.00",
    "high_price": "193.00",
    "low_price": "189.50",
    "volume": 1200000
  },
  "price_history": [
    {
      "price": "192.45",
      "timestamp": "2025-08-13T14:30:00Z",
      "open_price": "190.00",
      "high_price": "193.00",
      "low_price": "189.50",
      "volume": 1200000
    },
   
  ]
}
```

**Error Response:**
```json
{
  "error": "Stock with symbol {symbol} not found"
}
```

---

# Alerts API

## 1. List User Alerts

**Endpoint:**  
`GET /alerts/`

**Description:**  
Returns all alerts created by the authenticated user.

**Headers:**
```
Authorization: Bearer <your_token>
```

**Response:**
```json
{
    "id": 1,
    "stock": 1,
    "stock_details": {
        "id": 1,
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "is_active": true,
        "created_at": "2025-08-12T20:33:02.346493Z"
    },
    "user_email": "ganaasryyy061@gmail.com",
    "alert_type": "threshold",
    "condition_type": "above",
    "target_price": "200.00",
    "duration_minutes": null,
    "status": "active",
    "is_active": true,
    "email_notification": true,
    "created_at": "2025-08-13T17:38:48.076262Z",
    "updated_at": "2025-08-13T17:38:48.076324Z",
    "triggered_at": null
}
```

---

## 2. Create Alert

**Endpoint:**  
`POST /alerts/create/`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Request Body:**
```json
{
  "stock": 1,
  "alert_type": "threshold",
  "condition_type": "above",
  "target_price": "200.00",
  "duration_minutes": null,
  "email_notification": true
}
```

**Response:**
```json
{
  "id": 2,
  "stock": 1,
  "user_email": "user@example.com",
  "alert_type": "threshold",
  "condition_type": "above",
  "target_price": "200.00",
  "duration_minutes": null,
  "status": "active",
  "is_active": true,
  "email_notification": true,
  "created_at": "2025-08-14T10:00:00.000000Z",
  "updated_at": "2025-08-14T10:00:00.000000Z",
  "triggered_at": null
}
```

---

## 3. Update Alert

**Endpoint:**  
`PUT /alerts/{alert_id}/`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Request Body:**  
(Any fields you want to update, e.g.)
```json
{
  "target_price": "210.00",
  "condition_type": "below"
}
```

**Response:**
```json
{
  "id": 1,
  "stock": 1,
  "user_email": "user@example.com",
  "alert_type": "threshold",
  "condition_type": "below",
  "target_price": "210.00",
  "duration_minutes": null,
  "status": "active",
  "is_active": true,
  "email_notification": true,
  "created_at": "2025-08-13T17:38:48.076262Z",
  "updated_at": "2025-08-14T10:05:00.000000Z",
  "triggered_at": null
}
```

---

## 4. Delete Alert

**Endpoint:**  
`DELETE /alerts/{alert_id}/delete/`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Response:**
- **204 No Content**

---

## 5. Alert History

**Endpoint:**  
`GET /alert-history/`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Response:**
```json
{
    "id": 1,
    "alert": 1,
    "triggered_at": "2025-08-13T18:00:00.000000Z",
    "status": "triggered"
}
```

---

## 6. Notification Log

**Endpoint:**  
`GET /notification-log/`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Response:**
```json
{
    "id": 1,
    "user": 1,
    "alert": 1,
    "message": "Alert triggered for AAPL at $200.00",
    "sent_at": "2025-08-13T18:00:01.000000Z"
}
```
Or, if no notifications:
```json
{
  "message": "No notifications found for this user."
}
```

---

> **Note:** All alert endpoints require authentication. Always include your JWT token in the `Authorization` header.