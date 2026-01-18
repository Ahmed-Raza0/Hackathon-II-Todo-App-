# Quickstart Guide: Account Signup Implementation

## Overview
This guide explains how to implement and validate the account signup functionality following the SP-AUTH-ACCOUNT-CREATION specification.

## Prerequisites
- Backend API running with authentication endpoints
- Frontend development environment set up
- Required environment variables configured (BETTER_AUTH_SECRET, DATABASE_URL)
- No existing Dockerfile (using Python Space mode)

## Required Files Structure
```
/backend
 ├── main.py              # Entry point with 'app' variable
 ├── requirements.txt     # Dependencies including fastapi, uvicorn, etc.
 ├── src/
 │   ├── routes/
 │   │   └── auth.py     # Authentication endpoints
 │   └── app/
 │       └── layout.tsx  # For frontend
 /frontend
 ├── src/
 │   ├── app/
 │   │   ├── layout.tsx
 │   │   └── signup/
 │   │       └── page.tsx
 │   ├── lib/
 │   │   └── api.ts      # API client with signup function
 │   └── components/
 │       └── Header.tsx
 ├── tailwind.config.ts
 ├── postcss.config.js
 └── package.json
```

## Implementation Steps

### Step 1: Verify Backend Entry Point
1. Ensure `/backend/main.py` exists with proper app export:
```python
from fastapi import FastAPI

app = FastAPI(title="Todo API")

# Add routes here
```

### Step 2: Implement Signup Endpoint
1. Create POST /api/auth/signup endpoint in backend
2. Ensure it accepts {email, password} in request body
3. Verify it returns proper success/error responses as specified

### Step 3: Update Frontend Signup Form
1. Verify signup form calls backend API correctly
2. Ensure it handles structured error responses
3. Confirm loading states are properly implemented

### Step 4: Test Integration
1. Test successful signup flow
2. Test duplicate email scenario
3. Test weak password scenario
4. Verify error messages are properly displayed

## Validation Checklist
- [x] main.py exists at backend root with 'app' export
- [x] requirements.txt includes fastapi, uvicorn, and other dependencies
- [x] POST /api/auth/signup endpoint exists with proper contract
- [x] Frontend signup form calls backend API correctly
- [x] Structured error responses are returned for all failure cases
- [x] Header is hidden on signup page
- [x] Environment variables are properly configured
- [x] No hardcoded ports in configuration
- [x] Tailwind CSS is properly applied to signup page
- [x] Authentication token is returned on successful signup

## Common Issues and Solutions

### Issue: Build Fails on Hugging Face
**Symptoms**: Hugging Face Space build doesn't start
**Solution**:
- Verify main.py exists at root level
- Confirm app variable is exported
- Check requirements.txt has proper dependencies

### Issue: Signup Returns Generic Error
**Symptoms**: "Failed to create account. Please try again." message
**Solution**:
- Check that backend returns structured error responses
- Verify {error, code} fields are present in all error responses
- Confirm frontend displays backend error messages

### Issue: Header Shows on Auth Pages
**Symptoms**: Navigation header visible on signup page
**Solution**:
- Verify conditional header rendering logic
- Confirm signup page doesn't include header component

### Issue: Duplicate Email Not Handled
**Symptoms**: Unclear error when email already exists
**Solution**:
- Ensure backend properly detects duplicate emails
- Return specific error message for duplicate email case
- Frontend displays specific message to user

## Environment Variables for Hugging Face
- BETTER_AUTH_SECRET: Secret key for authentication
- DATABASE_URL: Connection string for database
- These must be set in Hugging Face Space settings

## Testing the Implementation
1. Try to create an account with valid email and strong password
2. Verify successful account creation and login
3. Try to create an account with duplicate email
4. Verify appropriate error message is displayed
5. Try to create an account with weak password
6. Verify appropriate error message is displayed
7. Confirm header is hidden on signup page
8. Verify all styling is properly applied via Tailwind