# Feature Specification: Full-Stack Todo Web App

**Feature Branch**: `001-fullstack-todo-app`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "# Phase II – Full‑Stack Todo Web App

## SP‑01: Overview

This Specification (SP) defines the **authoritative, implementation‑binding requirements** for **Phase II** of the Todo Application, in strict compliance with the **Todo App Constitution**. No implementation may diverge from this SP.

---

## SP‑02: Goals

* Convert console Todo app into a **secure, multi‑user web application**
* Ensure **data persistence**, **user isolation**, and **JWT‑based authentication**
* Provide a clean, responsive UI backed by a RESTful API

---

## SP‑03: Tech Stack (Locked)

| Layer    | Technology           |
| -------- | -------------------- |
| Frontend | Next.js (App Router) |
| Styling  | Tailwind CSS         |
| Backend  | FastAPI              |
| ORM      | SQLModel             |
| Database | Neon PostgreSQL      |
| Auth     | Better Auth + JWT    |

---

## SP‑04: Repository Structure (Monorepo)

\`\`\`
/todo-app
 ├── frontend/
 │   ├── app/
 │   ├── components/
 │   ├── lib/api.ts
 │   └── tailwind.config.ts
 ├── backend/
 │   ├── api/
 │   ├── models/
 │   ├── routes/
 │   ├── core/config.py
 │   └── main.py
 ├── specs/
 │   └── phase-2.md
 └── README.md
\`\`\`

---

## SP‑05: Data Models

### Task Model

\`\`\`ts
Task {
  id: UUID
  title: string (1–200)
  description?: string
  completed: boolean = false
  user_id: UUID (immutable)
  created_at: datetime
  updated_at: datetime
}
\`\`\`

**Invariants**

* \`user_id\` cannot be modified
* No task may exist without an owner

---

## SP‑06: API Contract

### Authentication

* JWT required on all endpoints
* Header: \`Authorization: Bearer <token>\`

---

### Endpoints

#### Create Task

\`\`\`
POST /api/tasks
\`\`\`

Request:

\`\`\`json
{ \"title\": \"Buy groceries\" }
\`\`\`

Response:

\`\`\`json
{ \"id\": \"uuid\", \"title\": \"Buy groceries\", \"completed\": false }
\`\`\`

---

#### List Tasks

\`\`\`
GET /api/tasks
\`\`\`

Returns only tasks belonging to authenticated user.

---

#### Update Task

\`\`\`
PUT /api/tasks/{task_id}
\`\`\`

---

#### Complete Task

\`\`\`
PATCH /api/tasks/{task_id}/complete
\`\`\`

---

#### Delete Task

\`\`\`
DELETE /api/tasks/{task_id}
\`\`\`

---

## SP‑07: Authorization Rules

* JWT user_id must match task.user_id
* Cross‑user access → **403 Forbidden**
* Missing or invalid token → **401 Unauthorized**

---

## SP‑08: Frontend Behavior

* Server Components by default
* Client Components only for forms and buttons
* API calls via \`/lib/api.ts\`
* Optimistic UI allowed but DB remains source of truth

---

## SP‑09: Error Handling

All errors return JSON:

\`\`\`json
{
  \"error\": \"string\",
  \"code\": \"TASK_NOT_FOUND\"
}
\`\`\`

No stack traces exposed.

---

## SP‑10: Quality Gates

* All endpoints manually tested
* Auth enforced on every route
* DB migrations reproducible
* UI verified on desktop + mobile

---

## SP‑11: Phase II Completion Criteria

Phase II is complete when:

* Users can register and login
* Tasks persist after reload
* User data is fully isolated
* System fully complies with Constitution

---

## SP‑12: Enforcement Clause

If implementation conflicts with this SP or the Constitution, **the spec must be corrected first**, then code regenerated.

---
"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - User Registration and Login (Priority: P1)

As a new user, I want to register for an account and log in so that I can access my personal todo list securely.

**Why this priority**: This is the foundation of the multi-user system and enables all other functionality. Without authentication, users cannot have isolated data.

**Independent Test**: Can be fully tested by registering a new user account, logging in, and verifying that a secure session is established. This delivers the core value of enabling personalized todo management.

**Acceptance Scenarios**:

1. **Given** I am a new visitor to the website, **When** I navigate to the registration page and complete the registration form, **Then** I should receive confirmation of successful registration and be logged in.
2. **Given** I have an existing account, **When** I navigate to the login page and enter my credentials, **Then** I should be authenticated and redirected to my todo dashboard.

---

### User Story 2 - Create and Manage Tasks (Priority: P2)

As a registered user, I want to create, view, update, and delete my tasks so that I can manage my personal todo list effectively.

**Why this priority**: This is the core functionality of the todo application. After authentication, this is the primary value proposition.

**Independent Test**: Can be fully tested by logging in as a user, creating tasks, viewing them, updating them, and deleting them. This delivers the core value of task management functionality.

**Acceptance Scenarios**:

1. **Given** I am logged in as a user, **When** I submit a new task with a title, **Then** the task should be created and visible in my task list.
2. **Given** I have existing tasks, **When** I update a task's details, **Then** the changes should be saved and reflected in my task list.
3. **Given** I have existing tasks, **When** I mark a task as complete, **Then** the task should be updated to reflect its completed status.

---

### User Story 3 - Secure Data Isolation (Priority: P3)

As a user, I want my tasks to be visible only to me so that my personal information remains private and secure.

**Why this priority**: While important for security, this is validation of a system-level requirement that should work transparently to the user.

**Independent Test**: Can be tested by having multiple users create accounts and tasks, then verifying that each user only sees their own tasks. This delivers the value of secure multi-user functionality.

**Acceptance Scenarios**:

1. **Given** I am logged in as User A with my tasks, **When** I access the task listing endpoint, **Then** I should only see tasks associated with my user account.
2. **Given** Another user (User B) has created tasks, **When** I attempt to access User B's tasks, **Then** I should receive a 403 Forbidden error or see no unauthorized data.

---

### Edge Cases

- What happens when a user attempts to access a task that doesn't exist or belongs to another user?
- How does system handle malformed JWT tokens or expired authentication?
- What occurs when a user tries to create a task with an empty title or a title exceeding 200 characters?
- How does the system behave when database connection is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register accounts with unique email addresses
- **FR-002**: System MUST authenticate users via JWT tokens following Better Auth standards
- **FR-003**: Users MUST be able to create tasks with titles between 1 and 200 characters
- **FR-004**: System MUST persist tasks in Neon PostgreSQL database with SQLModel ORM
- **FR-005**: System MUST enforce user data isolation - users can only access their own tasks
- **FR-006**: System MUST provide a RESTful API with endpoints for task CRUD operations
- **FR-007**: System MUST return structured JSON error responses for all error conditions
- **FR-008**: Users MUST be able to mark tasks as completed/incomplete via PATCH endpoint
- **FR-009**: System MUST validate that user_id in JWT matches task ownership for all operations

### Key Entities

- **User**: Represents a registered user with authentication credentials managed by Better Auth
- **Task**: Represents a todo item owned by a specific user, with properties for title, description, completion status, and timestamps

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can register and log in within 2 minutes of visiting the site
- **SC-002**: Users can create, view, update, and delete tasks with response times under 2 seconds
- **SC-003**: 100% of users who register successfully complete at least one task operation
- **SC-004**: Zero cross-user data access incidents occur during testing with multiple concurrent users
- **SC-005**: System maintains 99% uptime during peak usage hours