# API Documentation

## Base URL
```
http://localhost:8000/api/
```

---

## **Authentication**

Most endpoints require authentication using a JWT token.  
**Public endpoints:**  
- `/signup`
- `/forgot_password`
- `/reset_password/<token>`

**Protected endpoints:**  
- `/current_user`
- `/update_user`
- All `/stocks/*` endpoints

**How to Authenticate:**  
Include your token in the `Authorization` header:
```
Authorization: Bearer <your_token>
```

---

## **1. Sign Up**
Create a new user account.

**Endpoint:**  
`POST /signup`

**Request Body:**
```json
{
    "first_name": "Nour",
    "last_name": "ELmasry",
    "email": "NourElmasry123@gmail.com",
    "password": "mypassword123"
}
```

**Responses:**
- **201 Created**
    ```json
    {
        "details": "User created successfully."
    }
    ```
- **400 Bad Request**
    ```json
    {
        "error": "User with this email already exists."
    }
    ```

---

## **2. Get Current User**
Retrieve details of the authenticated user.

**Endpoint:**  
`GET /current_user`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Response:**
```json
{
    "id": 1,
    "first_name": "Nour",
    "last_name": "Elmasry",
    "email": "NourELmasry123@gmail.com"
}
```

---

## **3. Update User**
Update the authenticated user’s profile.

**Endpoint:**  
`PUT /update_user`

**Headers:**
```
Authorization: Bearer <your_token>
```

**Request Body:**
```json
{
    "first_name": "Nour",
    "last_name": "Elmasry",
    "email": "NourElmasry123@gmail.com",
    "password": "newpassword123"
}
```
> To keep the password unchanged, send an empty string `""` for `"password"`.

**Response:**
```json
{
    "id": 1,
    "first_name": "Nour",
    "last_name": "Elmasry",
    "email": "NourElmsry123@gmail.com"
}
```

---

## **4. Forgot Password**
Send a password reset email.

**Endpoint:**  
`POST /forgot_password`

**Request Body:**
```json
{
    "email": "NourELmasry123@gmail.com"
}
```

**Response:**
```json
{
    "details": "Password reset sent to NourElmasry123@gmail.com"
}
```

---

## **5. Reset Password**
Reset password using the token sent via email.

**Endpoint:**  
`POST /reset_password/<token>`

**Request Body:**
```json
{
    "password": "newpassword123",
    "confirmPassword": "newpassword123"
}
```

**Responses:**
- **200 OK**
    ```json
    {
        "details": "Password reset done"
    }
    ```
- **400 Bad Request** (Expired token)
    ```json
    {
        "error": "Token is expired"
    }
    ```
- **400 Bad Request** (Password mismatch)
    ```json
    {
        "error": "Password are not same"
    }
    ```

---

## **6. Logout**
Invalidate the current user's authentication token.

**Endpoint:**  

```
POST /logout
```

**Headers:**
```
Authorization: Bearer <your_reresh_token>
```

**Response:**
```json
{
    "details": "Successfully logged out."
}
```

---

## **Fetched Stock**

### **1. Fetch Stock Price**
Get the latest price for a specific stock symbol.

**Endpoint:**  
`GET /stocks/{symbol}`


**Response:**
```json
{
    "symbol": "AAPL",
    "price": 192.45,
    "currency": "USD",
    "timestamp": "2025-08-13T14:30:00Z"
}
```

---

### **2. List All Supported Stocks**
Get a list of all supported stock symbols.

**Endpoint:**  
`GET /stocks`


**Response:**
```json
[
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corporation"}
]
```


