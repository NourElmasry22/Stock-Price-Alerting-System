# API Documentation

## Base URL
```
http://localhost:8000/api/
```

---

## **1. Sign Up**
Create a new user account.

**Endpoint:**  
```
POST /signup
```

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
- **400 Bad Request** (Validation errors or email already exists)
```json
{
    "error": "User with this email already exists."
}
```

---

## **2. Get Current User**
Retrieve details of the currently authenticated user.

**Endpoint:**  
```
GET /current_user
```

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
Update current authenticated user’s profile.

**Endpoint:**  
```
PUT /update_user
```

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
> Send empty string `""` in `"password"` to keep it unchanged.

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
Send a password reset email with a token.

**Endpoint:**  
```
POST /forgot_password
```

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
Reset a user’s password using the token sent via email.

**Endpoint:**  
```
POST /reset_password/<token>
```

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

## **Authentication**
- Endpoints like `/current_user` and `/update_user` require **JWT** or **Token Authentication** depending on your project setup.
- Pass the token in the `Authorization` header as:
```
Authorization: Bearer <your_token>
```
