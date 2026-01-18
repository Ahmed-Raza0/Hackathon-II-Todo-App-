# SP-UIUX-PRO-BE – Backend Integration Specification (Frontend ↔ Backend)

This **SP-SPECIFY** extends **SP-UIUX-PRO** to explicitly define **frontend–backend integration requirements** so that **Add / Create actions work correctly**. This spec is binding and does **not** change backend logic; it defines **how the frontend must call it**.

## SP-UIUX-PRO-BE-01: Problem Statement

Current UI renders correctly, but **Add (Create) operations do not work** because:

* API client contract is undefined or inconsistent
* Auth token is not attached correctly
* Mutation success/failure states are not handled

This spec resolves all three.

## SP-UIUX-PRO-BE-02: Non‑Negotiable Rules

1. **Single API Client**: All frontend requests MUST go through one client.
2. **JWT Mandatory**: Every mutating request MUST include `Authorization: Bearer <token>`.
3. **Backend is Source of Truth**: UI updates only after API success.
4. **No Mock Writes**: Optimistic UI is allowed visually, but must reconcile with backend response.

## SP-UIUX-PRO-BE-03: API Client Specification

### File (Mandatory)

```
/frontend/src/lib/api.ts
```

### Responsibilities

* Attach JWT token to every request
* Centralize base URL
* Normalize error handling

### Required Shape

```ts
export async function api<T>(
  path: string,
  options: RequestInit = {}
): Promise<T>
```

## SP-UIUX-PRO-BE-04: Authentication Attachment Rule

* Token MUST be read from a single auth source (cookie or storage)
* Header format:

```
Authorization: Bearer <token>
```

Requests without token → **guaranteed failure**

## SP-UIUX-PRO-BE-05: Add (Create Task) Contract

### Backend Endpoint (Assumed Stable)

```
POST /api/tasks
```

### Request (Frontend MUST send)

```json
{
  "title": "string",
  "description": "string?"
}
```

### Success Response (Required)

```json
{
  "id": "uuid",
  "title": "string",
  "completed": false
}
```

## SP-UIUX-PRO-BE-06: Frontend Add Flow (Authoritative)

1. User submits Add form
2. UI enters loading state (button disabled)
3. `api('/api/tasks', { method: 'POST', body })`
4. Await backend response
5. On success:

   * Clear input
   * Refresh task list OR append returned task
6. On failure:

   * Show error message
   * Do NOT update UI state

## SP-UIUX-PRO-BE-07: Error Handling Rules

* 401 → redirect to login
* 403 → show permission error
* 4xx/5xx → human-readable error

No raw error dumps allowed.

## SP-UIUX-PRO-BE-08: Framer Motion Interaction Rules (Add)

* Button tap animation allowed
* Loading spinner animation allowed
* Success animation allowed (subtle)

Motion MUST NOT mask backend failure.

## SP-UIUX-PRO-BE-09: Validation Checklist

* Add task creates record in DB
* Page reload shows new task
* No task added without backend success
* JWT present on request

## SP-UIUX-PRO-BE-10: Supremacy Clause

Hierarchy:

**Constitution > Backend API Spec > SP-SRC > SP-FRONTEND-NEG > SP-UIUX-PRO > SP-UIUX-PRO-BE**

If Add does not work, this spec must be checked before code changes.

---

## User Scenarios & Testing

### Scenario 1: User Adds a New Task
**Given**: User is authenticated and on the tasks page
**When**: User fills out the task form and clicks "Add Task"
**Then**: The task is sent to the backend API with proper authentication
**Validation**: The API client attaches JWT token and handles success/failure appropriately

### Scenario 2: API Request Fails Due to Authentication
**Given**: User attempts to add a task with invalid/expired authentication
**When**: The API request is made with an invalid token
**Then**: User receives a 401 error and is redirected to login
**Validation**: Proper error handling prevents unauthorized requests

### Scenario 3: Successful Task Creation
**Given**: User submits a valid task with proper authentication
**When**: The POST request to /api/tasks is successful
**Then**: The new task appears in the task list
**Validation**: Backend returns the created task with ID, which updates the UI

## Functional Requirements

### FR-01: Centralized API Client
**Requirement**: The system shall have a single API client for all frontend requests.
**Acceptance Criteria**:
- All API calls go through the centralized client in `/frontend/src/lib/api.ts`
- The client handles authentication token attachment consistently
- Error handling is normalized across all requests

### FR-02: JWT Authentication
**Requirement**: Every mutating request must include a valid JWT token in the Authorization header.
**Acceptance Criteria**:
- The Authorization header is set to "Bearer <token>" for all mutating requests
- Token is retrieved from a single source (localStorage, cookie, or auth context)
- Requests without valid tokens fail gracefully

### FR-03: Task Creation Workflow
**Requirement**: The task creation flow must follow the specified sequence.
**Acceptance Criteria**:
- UI enters loading state when form is submitted
- POST request is made to `/api/tasks` with proper payload
- On success: input is cleared and task list is refreshed
- On failure: error message is shown and UI state is unchanged

### FR-04: Error Handling
**Requirement**: The system shall handle different error types appropriately.
**Acceptance Criteria**:
- 401 errors trigger redirect to login page
- 403 errors show permission error message
- 4xx/5xx errors show human-readable messages (no raw dumps)
- UI state is preserved during error conditions

## Success Criteria

### Quantitative Measures
- 100% of task creation requests include proper JWT authentication
- 0% of requests bypass the centralized API client
- 100% of API errors are handled with human-readable messages
- 95% success rate for valid task creation requests

### Qualitative Measures
- Users can successfully add tasks to their list
- Authentication is seamless during task creation
- Error states are clearly communicated to users
- UI provides appropriate feedback during loading states

## Key Entities

### API Client
- **Purpose**: Centralized request handler
- **Location**: `/frontend/src/lib/api.ts`
- **Responsibilities**: Token attachment, error normalization, base URL management

### Task Object
- **Structure**: {id: uuid, title: string, completed: boolean}
- **Creation**: Via POST to `/api/tasks` endpoint
- **Validation**: Title field is required, description is optional

## Assumptions

- Backend API endpoints are stable and follow REST conventions
- JWT tokens are stored securely in browser storage or cookies
- The backend properly validates authentication tokens
- Network connectivity is available during API requests

## Constraints

- All API requests must go through the single client implementation
- JWT tokens must be attached to mutating requests only
- Error messages must be user-friendly, not technical dumps
- UI updates only after successful backend responses

## Dependencies

- Backend API availability and stability
- Authentication system providing valid JWT tokens
- Frontend authentication context providing token access
- Network connectivity for API communication