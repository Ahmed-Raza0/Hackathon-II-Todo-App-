---
id: 1
title: Backend Frontend Integration Spec
stage: spec
date_iso: 2026-01-20
surface: agent
model: qwen-2.5-72b-instruct
feature: 005-backend-frontend-integration
branch: 005-backend-frontend-integration
user: Claude
command: sp.specify
labels: ["integration", "backend", "frontend", "auth", "cors", "api"]
links:
  spec: /mnt/d/Hackathon II (Todo App)/specs/005-backend-frontend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-backend-frontend-integration/spec.md
  - specs/005-backend-frontend-integration/checklists/requirements.md
  - history/prompts/005-backend-frontend-integration/001-backend-frontend-integration-spec.spec.prompt.md
tests: []
---

# Backend Frontend Integration Spec

## Summary

Created comprehensive specification for backend-frontend integration and error resolution. The specification defines requirements for integrating FastAPI backend with Next.js frontend, ensuring proper authentication, CORS handling, API contract alignment, and error-free operation.

## Prompt Text

```
# sp.specify — Backend ↔ Frontend Integration & Error Resolution

This specification defines **how the FastAPI backend and Next.js frontend must integrate**, and how to resolve current backend errors blocking integration.

---

## 1. Purpose

Ensure:

* Backend runs without import/runtime errors
* Frontend can successfully communicate with backend
* Authentication, CORS, and API contracts align
* A single, validated integration flow exists

This spec does **not** add new features.

---

## 2. Backend Requirements (FastAPI)

### 2.1 Project Structure (MANDATORY)

```
backend/
 ├── main.py
 ├── db.py
 ├── models.py
 ├── auth.py
 ├── deps.py
 ├── routes/
 │    ├── auth.py
 │    └── tasks.py
 └── .env
```

### 2.2 main.py (ASGI entrypoint)

* MUST expose: `app = FastAPI()`
* MUST include:

  * CORS middleware
  * Auth router
  * Task router

**Failure condition:**

> `Error loading ASGI app. Could not import module "main"`

This error means:

* `main.py` missing
* Wrong working directory
* Import error inside main.py

---

## 3. Environment Configuration

### Backend `.env`

```
DATABASE_URL=postgresql+psycopg2://user:pass@ep-xxxx.neon.tech/dbname
JWT_SECRET=change_me
CORS_ORIGINS=http://localhost:3000
```

* `.env` must load via `python-dotenv`

---

## 4. CORS (CRITICAL FOR INTEGRATION)

FastAPI MUST include:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
```

Without this:
❌ Frontend requests will fail

---

## 5. API Contract Alignment

### Auth Endpoints (Backend)

| Method | Path             | Purpose      |
| ------ | ---------------- | ------------ |
| POST   | /api/auth/signup | Create user  |
| POST   | /api/auth/login  | Login        |
| POST   | /api/auth/logout | Logout       |
| GET    | /api/auth/me     | Current user |

### Task Endpoints

| Method | Path            | Purpose     |
| ------ | --------------- | ----------- |
| GET    | /api/tasks      | List tasks  |
| POST   | /api/tasks      | Create task |
| PUT    | /api/tasks/{id} | Update      |
| DELETE | /api/tasks/{id} | Delete      |

Frontend MUST use exactly these paths.

---

## 6. Frontend Requirements (Next.js App Router)

### 6.1 Environment

`.env.local`

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 6.2 Fetch Rules

* All requests must include `credentials: "include"`
* Base URL must come from env

Example:

```ts
fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
  credentials: "include"
})
```

---

## 7. Integration Flow (Happy Path)

1. User opens `/login`
2. Frontend → POST `/api/auth/login`
3. Backend sets httpOnly cookie
4. Frontend redirects → `/dashboard`
5. `/dashboard` fetches `/api/tasks`
6. Tasks returned (user-scoped)

---

## 8. Validation Checklist

* [ ] `uvicorn main:app --reload` works
* [ ] No import errors
* [ ] CORS allows localhost:3000
* [ ] Auth endpoints reachable from browser
* [ ] Tasks fetch works with cookie

---

## 9. Out of Scope

* AI / MCP
* UI styling
* Phase III features

---

## Completion Gate

Backend + Frontend must communicate successfully with authentication enforced.
```

## Response Text

Successfully created the specification for backend-frontend integration and error resolution. The specification includes:

- Three user stories with clear acceptance criteria
- Twelve functional requirements covering backend stability, CORS, authentication, API contracts, and error handling
- Seven measurable success criteria with specific metrics
- Proper entity definitions for user session and API request
- Clear edge case handling

The specification follows all requirements and is ready for the planning phase. It addresses the critical need to resolve backend errors and establish proper communication between frontend and backend components.

## Outcome

The feature specification is complete and ready for the next phase of planning. It provides clear requirements for implementing the integration between backend and frontend while addressing current error conditions.