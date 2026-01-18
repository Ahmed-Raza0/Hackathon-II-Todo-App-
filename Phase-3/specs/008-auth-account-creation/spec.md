# SP-AUTH-ACCOUNT-CREATION – Account Signup Failure Resolution Specification

This **SP-SPECIFY** authoritatively defines how **account creation (Sign Up)** must work end‑to‑end and resolves the error:

> **"Failed to create account. Please try again."**

This spec is binding for **frontend + backend + auth provider (Better Auth / Hugging Face)**.

---

## SP-AUTH-01: Problem Statement

Observed behavior:

• User fills signup form correctly
• Submit request is sent
• UI shows generic error: *Failed to create account*
• No clear reason shown

This means **signup request is failing at backend or auth layer**, not UI only.

---

## SP-AUTH-02: Non‑Negotiable Rules

1. **No Generic Failures** – Signup MUST return a structured error reason
2. **Auth Provider is Authority** – Backend does NOT fake success
3. **Frontend Shows Backend Truth** – No masking of auth errors
4. **One Signup Path Only** – No duplicate signup logic

---

## SP-AUTH-03: Canonical Signup Flow (Authoritative)

### Flow

1. Frontend submits signup form
2. Request sent to backend auth endpoint
3. Backend calls Better Auth
4. Better Auth creates user
5. Backend returns success or exact failure
6. Frontend reacts accordingly

---

## SP-AUTH-04: Backend Signup Contract

### Endpoint (Required)

```
POST /api/auth/signup
```

### Request Body

```json
{
  "email": "string",
  "password": "string"
}
```

### Success Response

```json
{
  "user": {
    "id": "uuid",
    "email": "string"
  },
  "token": "jwt"
}
```

---

## SP-AUTH-05: Failure Response Contract (CRITICAL)

### Backend MUST return

```json
{
  "error": "string",
  "code": "AUTH_SIGNUP_FAILED"
}
```

❌ Returning empty 400/500 is FORBIDDEN

---

## SP-AUTH-06: Common Failure Causes (Root Truth)

| Cause                | Explanation                  |
| -------------------- | ---------------------------- |
| Email already exists | Auth provider rejected       |
| Weak password        | Policy violation             |
| Missing secret       | `BETTER_AUTH_SECRET` not set |
| HF env missing       | Env vars not configured      |
| Wrong endpoint       | Frontend calling wrong route |

---

## SP-AUTH-07: Frontend Signup Handling Rules

### Frontend MUST:

• Await backend response
• Parse `error` field
• Display error message to user
• NOT show generic message unless backend gives none

---

## SP-AUTH-08: Hugging Face Environment Rules

For signup to work on HF, these MUST exist:

```
BETTER_AUTH_SECRET
DATABASE_URL
```

❌ Missing any → signup ALWAYS fails

---

## SP-AUTH-09: Logging & Debug Rule

Backend MUST log:

• Signup request received
• Auth provider response
• Exact failure reason

Logs MUST NOT expose passwords.

---

## SP-AUTH-10: Validation Checklist

✔ Signup creates user in DB
✔ Duplicate email rejected with message
✔ Frontend shows real error
✔ JWT returned on success

---

## SP-AUTH-11: Supremacy Clause

Hierarchy:

**Constitution > Auth Spec > SP-AUTH-ACCOUNT-CREATION > Code**

If signup fails, check this spec before UI changes.

---

**End of SP-AUTH-ACCOUNT-CREATION Specification**

## User Scenarios & Testing

### Scenario 1: Successful Account Creation
**Given**: User provides valid email and strong password
**When**: User submits signup form
**Then**: Account is created and user is logged in
**Validation**: Backend returns success response with JWT token and user data

### Scenario 2: Duplicate Email Attempt
**Given**: User tries to sign up with an email that already exists
**When**: User submits signup form with duplicate email
**Then**: User receives specific error message about email being taken
**Validation**: Backend returns structured error response with clear message

### Scenario 3: Weak Password Attempt
**Given**: User tries to sign up with a weak password
**When**: User submits signup form with weak password
**Then**: User receives specific error message about password requirements
**Validation**: Backend validates password strength and returns appropriate error

### Scenario 4: Missing Environment Variables
**Given**: Backend is missing required environment variables
**When**: User submits signup form
**Then**: User receives server error with appropriate message
**Validation**: Backend logs the configuration issue and returns proper error response

## Functional Requirements

### FR-01: Account Creation Endpoint
**Requirement**: The system must provide a dedicated endpoint for creating new user accounts.
**Acceptance Criteria**:
- POST /api/auth/signup endpoint exists and accepts email/password
- Response includes user data and authentication token on success
- Proper validation of email format and password strength
- Returns structured error responses on failure

### FR-02: Error Handling
**Requirement**: The system must return structured error messages for all failure scenarios.
**Acceptance Criteria**:
- All error responses include both 'error' and 'code' fields
- Specific error messages for different failure types (duplicate email, weak password, etc.)
- No generic error responses that mask the actual issue
- Proper HTTP status codes for different error types

### FR-03: Frontend-Backend Integration
**Requirement**: The frontend must properly handle signup responses from the backend.
**Acceptance Criteria**:
- Frontend awaits backend response before showing any message
- Error messages from backend are displayed to the user
- Success responses result in proper authentication state setup
- Loading states are properly managed during signup request

### FR-04: Authentication Provider Integration
**Requirement**: The backend must properly integrate with the authentication provider.
**Acceptance Criteria**:
- Better Auth (or equivalent) is properly configured
- User data is correctly passed between backend and auth provider
- JWT tokens are properly handled and returned
- All auth provider responses are properly processed

### FR-05: Environment Configuration Validation
**Requirement**: The system must validate required environment variables before processing signup requests.
**Acceptance Criteria**:
- Backend verifies presence of required environment variables
- Clear error messages when configuration is missing
- No signup attempts made without proper configuration
- Proper logging of configuration validation results

## Success Criteria

### Quantitative Measures
- 100% of successful signup attempts create a user account in the database
- 100% of error responses contain structured error information
- 0% of signup requests result in unhandled exceptions
- 95% success rate for valid signup requests with proper data
- Error response time under 2 seconds for all failure scenarios

### Qualitative Measures
- Users receive clear, actionable feedback when signup fails
- Signup process is intuitive and guides users toward success
- Authentication state is properly managed after successful signup
- Error messages help users understand and resolve issues
- Integration between frontend and backend is seamless

## Key Entities

### User Account
- **Location**: Database managed by authentication provider
- **Purpose**: Store user identity and authentication information
- **Fields**: id (UUID), email (string), password (hashed), timestamps
- **Constraints**: Email must be unique, password must meet strength requirements

### Authentication Token
- **Location**: Generated by auth provider and returned to frontend
- **Purpose**: Maintain authenticated session after signup
- **Format**: JWT token with appropriate claims
- **Constraints**: Must be properly secured and have appropriate expiration

### Signup Request
- **Location**: /api/auth/signup endpoint
- **Purpose**: Handle new account creation requests
- **Structure**: Contains email and password with proper validation
- **Constraints**: Must validate data before sending to auth provider

## Assumptions

- The authentication provider (Better Auth or similar) is properly configured and accessible
- Required environment variables (BETTER_AUTH_SECRET, DATABASE_URL) are set correctly
- The frontend is using the centralized API client for all requests
- Network connectivity exists between frontend and backend
- The backend server is properly configured to handle CORS requests from the frontend

## Constraints

- Only one signup endpoint is allowed (no duplicate signup logic)
- Error responses must follow the specified structure with error and code fields
- Passwords must not be logged or exposed in any way
- All signup requests must go through proper authentication provider
- Frontend must not mask or replace backend error messages

## Dependencies

- Authentication provider service (Better Auth or equivalent)
- Database for storing user accounts
- Proper environment configuration with secrets
- Frontend API client implementation
- Network connectivity between components