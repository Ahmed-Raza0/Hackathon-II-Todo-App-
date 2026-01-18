# Feature Specification: Backend & Frontend Boot Fix

**Feature Branch**: `001-boot-fix`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "Backend & Frontend Boot Specification (SP‑FIX)

This SP **authoritatively specifies** the required backend and frontend boot structure for Phase III to eliminate:

* `Error loading ASGI app. Could not import module "main"`
* Frontend `404 – This page could not be found`

No fixes may be applied outside this spec.

---

## SP‑FIX‑01: Backend Boot Contract (FastAPI)

### Required File Structure

```
/backend
 ├── main.py          ← REQUIRED ENTRYPOINT
 ├── app/
 │   ├── __init__.py
 │   ├── api/
 │   ├── models/
 │   ├── core/
 │   └── db/
 ├── requirements.txt
 └── README.md
```

**Invariant**

* `main.py` MUST exist at `/backend/main.py`
* `main.py` MUST expose variable `app`

---

## SP‑FIX‑02: FastAPI Entry Definition

### main.py Specification

```python
from fastapi import FastAPI

app = FastAPI(title="Todo Phase III API")

@app.get("/health")
def health():
    return {"status": "ok"}
```

**Rules**

* Variable name MUST be `app`
* No conditional imports
* No relative execution assumptions

---

## SP‑FIX‑03: Uvicorn Execution Rule

### Allowed Command

```
uvicorn main:app --reload --port 8000
```

**Execution Context Rule**

* Command MUST be run from `/backend` directory
* `main.py` must be directly importable

---

## SP‑FIX‑04: Backend Failure Conditions

| Condition               | Result       |
| ----------------------- | ------------ |
| `main.py` missing       | Startup FAIL |
| `app` not defined       | Startup FAIL |
| Wrong working directory | Import FAIL  |

---

## SP‑FIX‑05: Frontend Boot Contract (Next.js)

### Required Structure (App Router)

```
/frontend
 ├── app/
 │   ├── layout.tsx
 │   ├── page.tsx     ← REQUIRED
 │   └── globals.css
 ├── tailwind.config.ts
 ├── next.config.js
 └── package.json
```

**Invariant**

* `/app/page.tsx` MUST exist
* Missing page.tsx results in 404

---

## SP‑FIX‑06: Root Page Specification

### page.tsx

```tsx
export default function Home() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Todo App Phase III</h1>
    </main>
  )
}
```

---

## SP‑FIX‑07: Frontend Failure Conditions

| Condition                    | Result          |
| ---------------------------- | --------------- |
| Missing `app/page.tsx`       | 404 Error       |
| Using pages/ instead of app/ | 404             |
| Wrong Next.js version        | Router mismatch |

---

## SP‑FIX‑08: Integration Validation

### Backend Validation

```
GET http://127.0.0.1:8000/health
→ 200 OK
```

### Frontend Validation

```
http://localhost:3000
→ Home page renders
```

---

## SP‑FIX‑09: Enforcement Clause

If runtime behavior deviates:

1. Specs are checked
2. Folder structure corrected
3. Code regenerated

Manual hot‑fixes are forbidden.

---

**End of SP‑FIX (Backend & Frontend Boot)**"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Backend App Startup (Priority: P1)

As a developer, I want the backend to start successfully so that I can run the API server without errors.

**Why this priority**: This is critical for the application to function. Without a working backend, no API functionality is available.

**Independent Test**: Can be fully tested by running `uvicorn main:app --reload --port 8000` from the `/backend` directory and verifying the server starts without errors. This delivers the core value of having a functional API server.

**Acceptance Scenarios**:

1. **Given** I am in the `/backend` directory with a properly configured `main.py`, **When** I run `uvicorn main:app --reload --port 8000`, **Then** the FastAPI server starts successfully on port 8000.
2. **Given** The backend server is running, **When** I make a GET request to `http://127.0.0.1:8000/health`, **Then** I receive a 200 OK response with status: "ok".

---

### User Story 2 - Frontend Page Rendering (Priority: P2)

As a user, I want to visit the homepage and see it render correctly so that I can use the application.

**Why this priority**: This ensures the frontend is functional and provides a basic user experience.

**Independent Test**: Can be fully tested by starting the Next.js development server and navigating to the root URL. This delivers the core value of having a functional frontend.

**Acceptance Scenarios**:

1. **Given** I have the frontend configured with a root page, **When** I run `npm run dev` and navigate to `http://localhost:3000`, **Then** the home page renders successfully without 404 errors.
2. **Given** The frontend is running, **When** I access the root route, **Then** I see the "Todo App Phase III" heading displayed.

---

### User Story 3 - Integrated System Validation (Priority: P3)

As a developer, I want both backend and frontend to work together so that I can develop and test integrated features.

**Why this priority**: This validates the complete system works as expected after the fixes.

**Independent Test**: Can be tested by running both backend and frontend servers and verifying they can communicate. This delivers the value of a fully functional development environment.

**Acceptance Scenarios**:

1. **Given** Both backend and frontend servers are running, **When** I make API calls from the frontend to the backend, **Then** the requests complete successfully.
2. **Given** The integrated system is running, **When** I perform basic functionality tests, **Then** both frontend and backend behave as expected.

---

### Edge Cases

- What happens when the main.py file is missing or incorrectly named?
- How does the system handle incorrect working directory when starting the backend?
- What occurs when the frontend app/page.tsx file is missing or incorrectly structured?
- How does the system behave when there are version mismatches between Next.js and the app router?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST have a main.py file at /backend/main.py that exposes an 'app' variable
- **FR-002**: System MUST allow the backend to be started with 'uvicorn main:app --reload --port 8000' command
- **FR-003**: Users MUST be able to access the backend health endpoint at /health
- **FR-004**: System MUST have a root page file at /frontend/app/page.tsx
- **FR-005**: System MUST render the frontend root page without 404 errors
- **FR-006**: System MUST follow the Next.js App Router structure requirements
- **FR-007**: System MUST allow both backend and frontend to run simultaneously without conflicts

### Key Entities

- **Backend App**: The FastAPI application instance that must be accessible as 'app' in main.py
- **Frontend Page**: The root page component that must exist in the Next.js App Router structure

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Backend server starts successfully with uvicorn command without errors
- **SC-002**: Health endpoint returns 200 OK status consistently
- **SC-003**: Frontend homepage renders without 404 errors
- **SC-004**: Both backend and frontend can run simultaneously in development mode
- **SC-005**: Development environment is stable with no boot-related errors