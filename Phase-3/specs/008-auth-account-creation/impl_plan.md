# SP-AUTH-ACCOUNT-CREATION – Implementation Plan (Account Signup Failure Resolution)

This **Implementation Plan** defines the step-by-step approach for implementing the **SP-AUTH-ACCOUNT-CREATION** specification to resolve account signup failures.

## Technical Context

The current state shows that the frontend and backend may have signup functionality that is failing due to improper integration with the authentication provider. The issue manifests as generic error messages when users try to create accounts. We need to ensure proper API contract implementation between frontend and backend for signup functionality.

## Constitution Check

The implementation aligns with the project constitution by:
- Following the non-negotiable rules of the SP-AUTH-ACCOUNT-CREATION specification
- Maintaining proper separation of frontend and backend concerns
- Enforcing the canonical folder structure
- Ensuring secure authentication flow with proper error handling

## Gates

### Gate 1: Pre-implementation Validation
- [x] SP-AUTH-ACCOUNT-CREATION specification is approved
- [x] Backend API is running and accessible
- [x] Frontend development environment is available

### Gate 2: Implementation Prerequisites
- [x] Node.js and npm are available
- [x] Python environment is accessible for backend
- [x] Required environment variables are configured

## Phase 0: Research & Analysis

### R0.1: Current Signup Implementation Assessment
**Task**: Research current signup form implementation and API integration
**Decision**: Need to understand how the current signup form works and how it connects to the backend
**Rationale**: Understanding current state is critical to implement the correct signup flow
**Alternatives considered**: Complete rewrite vs. enhancement of existing - chose to analyze first

### R0.2: API Contract Verification
**Task**: Research current API endpoint implementation for signup
**Decision**: Need to verify the current /api/auth/signup endpoint implementation
**Rationale**: Required to ensure proper contract compliance with the specification
**Alternatives considered**: Different endpoint patterns - chose to follow specification contract

### R0.3: Authentication Provider Integration
**Task**: Research current Better Auth integration pattern
**Decision**: Need to understand how the backend communicates with the auth provider
**Rationale**: Critical to ensure proper user creation flow through the auth provider
**Alternatives considered**: Different auth providers - chose to use existing Better Auth setup

## Phase 1: Design & Contracts

### Task 1: Verify main.py exists at root level with proper app export
**Location**: `/backend/main.py`
**Action**: Ensure file exists and exports the FastAPI app variable as 'app'
**Current Status**: NEEDS VERIFICATION

### Task 2: Create/verify signup API endpoint
**Location**: `/backend/src/routes/auth.py` or similar
**Action**: Implement POST /api/auth/signup endpoint following the specification contract
**Current Status**: NEEDS IMPLEMENTATION

### Task 3: Create/verify frontend signup form
**Location**: `/frontend/src/app/signup/page.tsx`
**Action**: Implement signup form that calls the backend API correctly
**Current Status**: NEEDS IMPLEMENTATION

### Task 4: Update API client for signup functionality
**Location**: `/frontend/src/lib/api.ts`
**Action**: Ensure authAPI includes signup function following the specification
**Current Status**: NEEDS VERIFICATION

### Task 5: Verify requirements.txt includes all necessary dependencies
**Location**: `/backend/requirements.txt`
**Action**: Ensure all required packages for auth functionality are included
**Current Status**: NEEDS VERIFICATION

## Data Model

### User Account Entity
- **Fields**: id (UUID), email (string), password (hashed), created_at (timestamp), updated_at (timestamp)
- **Constraints**: Email must be unique, password must meet strength requirements
- **Validation**: Email format validation, password strength validation

### Signup Request Entity
- **Fields**: email (string), password (string)
- **Validation**: Required fields, email format, password strength
- **Constraints**: No additional fields allowed in request

### Signup Response Entity
- **Success Fields**: user (object with id and email), token (JWT string)
- **Error Fields**: error (string), code (string)
- **Validation**: Proper structure for both success and error responses

## API Contracts

### POST /api/auth/signup
**Request**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response** (200):
```json
{
  "user": {
    "id": "uuid",
    "email": "string"
  },
  "token": "jwt"
}
```

**Error Response** (400/409/500):
```json
{
  "error": "string",
  "code": "AUTH_SIGNUP_FAILED"
}
```

## Quickstart Guide

### For Developers
1. Ensure main.py exists at backend root with proper app export
2. Verify requirements.txt includes all auth dependencies
3. Implement POST /api/auth/signup endpoint with proper error handling
4. Create signup form that calls the API with correct payload
5. Test signup flow with various scenarios (valid, duplicate email, weak password)

### Testing
1. Valid signup request creates user and returns token
2. Duplicate email returns proper error message
3. Weak password returns proper validation error
4. Missing fields return proper validation error
5. Frontend displays real backend errors to users