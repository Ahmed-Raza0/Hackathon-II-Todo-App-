# SP-FULL-INTEGRATION – Backend ↔ Frontend Integration & Build Specification

This **SP-SPECIFY** authoritatively defines how the **backend and frontend are integrated, run, and built together** for the Todo App. Its purpose is to eliminate **all integration, run, and build errors** permanently.

This spec is **binding** for both Phase II and Phase III execution.

---

## SP-FI-01: Purpose

This specification ensures:

• Frontend successfully communicates with backend
• JWT authentication works end-to-end
• Development servers run without errors
• Production build completes without failure
• No 404, CORS, or API mismatch issues

---

## SP-FI-02: Canonical Ports & URLs (LOCKED)

### Backend

```
http://127.0.0.1:8000
```

### Frontend

```
http://localhost:3000
```

❌ Changing ports without spec update is forbidden.

---

## SP-FI-03: Backend Contract (FastAPI)

### Backend MUST:

• Expose all APIs under `/api/*`
• Expose health endpoint:

```
GET /health → 200 OK
```

• Accept JWT via:

```
Authorization: Bearer <token>
```

• Enable CORS for frontend origin

### Required CORS Rule

```
allow_origins=["http://localhost:3000"]
```

---

## SP-FI-04: Frontend API Configuration

### Environment Variable (MANDATORY)

```
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### API Client Rule

All requests MUST be:

```
fetch(`${BASE_URL}/api/...`)
```

No hardcoded URLs allowed.

---

## SP-FI-05: Backend ↔ Frontend Data Flow

### Example: Add Task

1. User submits form (frontend)
2. Frontend calls:

   ```
   POST /api/tasks
   ```
3. Backend validates JWT
4. Backend writes to DB
5. Backend returns JSON
6. Frontend updates UI

Frontend MUST NOT update state before step 5.

---

## SP-FI-06: Error Resolution Matrix

| Error       | Root Cause               | Resolution       |
| ----------- | ------------------------ | ---------------- |
| 404 API     | Wrong base URL           | Use env var      |
| CORS error  | Missing middleware       | Enable CORS      |
| 401         | Token missing            | Attach JWT       |
| CSS missing | globals.css not imported | Fix layout.tsx   |
| Build fail  | Type error               | Fix before build |

---

## SP-FI-07: Development Run Order (MANDATORY)

### Step 1: Run Backend

```
cd backend
uvicorn main:app --reload --port 8000
```

### Step 2: Run Frontend

```
cd frontend
npm run dev
```

Backend MUST be running before frontend API calls.

---

## SP-FI-08: Production Build Rules

### Frontend Build

```
cd frontend
npm run build
```

Build MUST succeed with:

✔ No TypeScript errors
✔ No missing env variables

---

### Backend Check

```
python -m compileall .
```

No syntax errors allowed.

---

## SP-FI-09: Forbidden Patterns

❌ Frontend calling backend without `/api`
❌ Hardcoded localhost URLs
❌ Backend sessions/state
❌ Ignoring build errors

---

## SP-FI-10: Validation Checklist

✔ Backend `/health` reachable
✔ Frontend loads UI with CSS
✔ API calls succeed
✔ Tasks persist after reload
✔ `npm run build` passes

---

## SP-FI-11: Supremacy Clause

Hierarchy:

**Constitution > Backend Spec > SP-FRONTEND-REBUILD > SP-FULL-INTEGRATION > Code**

If integration fails, regenerate according to this spec.

---

**End of SP-FULL-INTEGRATION Specification**

## User Scenarios & Testing

### Scenario 1: User Logs In and Adds Task
**Given**: User has valid credentials and is on the login page
**When**: User submits login form and then adds a new task
**Then**: User is authenticated and task is persisted in the backend
**Validation**: API calls succeed with proper JWT tokens and data persists

### Scenario 2: User Views Task List
**Given**: User has authentication token and tasks exist in the backend
**When**: User navigates to the tasks page
**Then**: All tasks are loaded and displayed properly with correct styling
**Validation**: API call to fetch tasks succeeds and UI renders with Tailwind classes

### Scenario 3: User Updates Task Status
**Given**: User has a list of tasks and wants to mark one as completed
**When**: User toggles the completion status of a task
**Then**: The task status is updated in the backend and UI reflects the change
**Validation**: PUT/PATCH API call succeeds and returns updated task data

### Scenario 4: Session Expires During Activity
**Given**: User has been inactive for a while with a valid session
**When**: User tries to perform an authenticated action
**Then**: User is redirected to login page with appropriate message
**Validation**: 401 responses trigger proper logout and redirect flow

## Functional Requirements

### FR-01: API Communication Protocol
**Requirement**: The frontend must communicate with backend using standardized API endpoints.
**Acceptance Criteria**:
- All API requests use the NEXT_PUBLIC_API_BASE_URL environment variable
- JWT tokens are properly attached to authenticated requests
- All API endpoints follow the `/api/*` pattern as required
- Error responses are handled gracefully with user-friendly messages

### FR-02: Authentication Flow Integration
**Requirement**: The authentication system must work seamlessly between frontend and backend.
**Acceptance Criteria**:
- Login form successfully authenticates users with backend
- JWT tokens are stored securely and attached to subsequent requests
- Protected routes require valid authentication
- Logout properly clears authentication tokens

### FR-03: Task Management Integration
**Requirement**: Task CRUD operations must be properly integrated with backend APIs.
**Acceptance Criteria**:
- Creating tasks sends proper POST request to `/api/tasks`
- Retrieving tasks sends proper GET request to `/api/tasks`
- Updating tasks sends proper PUT/PATCH request to `/api/tasks/{id}`
- Deleting tasks sends proper DELETE request to `/api/tasks/{id}`

### FR-04: CORS Policy Enforcement
**Requirement**: Backend must properly configure CORS to allow frontend communication.
**Acceptance Criteria**:
- CORS policy allows requests from `http://localhost:3000`
- Preflight requests are properly handled
- No CORS errors occur during API communication

### FR-05: Build Process Validation
**Requirement**: Both frontend and backend must build successfully without errors.
**Acceptance Criteria**:
- Frontend builds with `npm run build` without TypeScript errors
- Backend compiles without syntax errors
- All environment variables are properly configured
- Production deployments function correctly

## Success Criteria

### Quantitative Measures
- 100% of API requests return successful responses (200/201/204)
- 0% of requests result in CORS or authentication errors
- 100% of build processes complete without compilation errors
- Page load time under 3 seconds for all routes
- 99% uptime for the health check endpoint

### Qualitative Measures
- Users can seamlessly navigate between authenticated and public routes
- UI appears professional with consistent styling across all pages
- All interactive elements respond appropriately to user actions
- Error states are handled gracefully with clear user feedback
- Authentication flow works reliably across different browsers

## Key Entities

### API Gateway
- **Location**: `/frontend/src/lib/api.ts` and backend API endpoints
- **Purpose**: Centralized communication layer between frontend and backend
- **Responsibilities**: Request routing, authentication token management, error handling

### Authentication Service
- **Location**: `/api/auth/*` endpoints on backend and auth context on frontend
- **Purpose**: User authentication and session management
- **Responsibilities**: Credential validation, JWT token generation, session management

### Task Management Service
- **Location**: `/api/tasks/*` endpoints on backend and task components on frontend
- **Purpose**: Task CRUD operations and state management
- **Responsibilities**: Task creation, retrieval, updates, deletion, and UI synchronization

## Assumptions

- The backend API is built with FastAPI and deployed at the canonical URL
- The frontend is built with Next.js using the App Router
- Users have modern browsers that support required web technologies
- Network connectivity is available for API communications
- Environment variables are properly configured in deployment environments

## Constraints

- All API communication must go through the centralized API client
- CORS policy must restrict access to only the frontend origin
- JWT tokens must be securely stored and transmitted
- Build processes must pass all validation checks before deployment
- No hardcoded URLs are allowed in the frontend codebase

## Dependencies

- FastAPI backend service for API endpoints
- Next.js framework for frontend routing
- Tailwind CSS for styling
- Authentication system for user management
- Database for data persistence