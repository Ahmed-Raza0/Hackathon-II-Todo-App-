# Data Model: Authentication Endpoints

## Overview
This document defines the authentication endpoint schema for the Todo application, separating public endpoints from protected endpoints.

## Public Authentication Endpoints

### Signup Endpoint
- **Method**: POST
- **Path**: `/api/auth/signup`
- **Access**: Public (no JWT required)
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string",
    "name": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user_id": "string",
    "email": "string",
    "name": "string",
    "token": "string"
  }
  ```

### Login Endpoint
- **Method**: POST
- **Path**: `/api/auth/login`
- **Access**: Public (no JWT required)
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user_id": "string",
    "email": "string",
    "name": "string",
    "token": "string"
  }
  ```

### Logout Endpoint
- **Method**: POST
- **Path**: `/api/auth/logout`
- **Access**: Public (JWT optional, but if provided, will be invalidated)
- **Request Body**: None
- **Response**: Empty response

## Protected Task Endpoints

### Task Operations
- **Paths**: `/api/{user_id}/*`
- **Access**: Requires valid JWT
- **Headers**: Authorization: Bearer {token}
- **User ID**: Extracted from JWT and validated against path parameter

## Auth Middleware Configuration

### Public Paths (No Auth Required)
- `/`
- `/health`
- `/ready`
- `/status`
- `/api/auth/signup`
- `/api/auth/login`
- `/api/auth/logout`
- `/docs`
- `/redoc`

### Protected Paths (Auth Required)
- `/api/{user_id}/*` (all task operations)
- All other authenticated user operations

## Security Requirements

### JWT Validation
- Token signature verification
- Expiration check
- User existence verification
- User ID matching between JWT and path parameters

### Input Validation
- Email format validation for auth endpoints
- Password strength requirements
- Rate limiting for auth endpoints