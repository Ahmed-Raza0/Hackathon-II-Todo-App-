---
id: 1
title: update-todo-app-constitution
stage: constitution
date: 2026-01-16
surface: agent
model: qwen-2.5-72b-instruct
feature: none
branch: main
user: unknown
command: /sp.constitution
labels: ["constitution", "todo-app", "spec-driven-development", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/0001-update-todo-app-constitution.constitution.prompt.md
tests:
 - none
---

## Prompt

# Todo App – Spec Constitution

This Constitution governs **Spec-Driven Development (SDD)** for the Todo application during **Phase II (Full‑Stack Web App)** and **Phase III (AI‑Powered Chatbot)**. It defines non‑negotiable rules, architectural principles, quality gates, and enforcement mechanisms that all specs and generated implementations must follow.

---

## Phase II – Full‑Stack Web Application Constitution

### 1. Purpose & Scope

Phase II transforms the in‑memory console app into a **secure, multi‑user, persistent web application**. The constitution ensures consistency across frontend (Next.js), backend (FastAPI), database (Neon PostgreSQL), and authentication (Better Auth + JWT).

**In Scope**

* Task CRUD (Add, View, Update, Delete, Complete)
* RESTful API
* Persistent storage
* Authentication & authorization
* Responsive UI

**Out of Scope**

* AI chatbot logic
* Kubernetes or cloud deployment
* Advanced task intelligence (recurring, reminders)

---

### 2. Non‑Negotiable Principles

1. **Spec First, Code Second**
   No code is written or regenerated unless a corresponding spec exists and is approved.
2. **User Isolation by Default**
   All data access is scoped to the authenticated user.
3. **Stateless Backend**
   FastAPI must not store session state; authentication relies solely on JWT.
4. **Single Source of Truth**
   Database is the authoritative state; frontend caches are ephemeral.
5. **Monorepo Consistency**
   Frontend and backend live in one repo with shared specs.

---

### 3. Architecture Mandates

#### 3.1 Frontend (Next.js)

* App Router (Server Components by default)
* Client Components only for interactivity
* Central API client (`/lib/api.ts`)
* Tailwind CSS only (no inline styles)

#### 3.2 Backend (FastAPI)

* All routes under `/api/`
* Pydantic models for all I/O
* SQLModel for ORM
* Environment‑based configuration

#### 3.3 Authentication

* Better Auth issues **JWT tokens**
* JWT included in `Authorization: Bearer <token>`
* Shared secret via `BETTER_AUTH_SECRET`

---

### 4. Data Constitution

#### 4.1 Core Entities

* **User** (managed by Better Auth)
* **Task** (owned by a user)

#### 4.2 Task Invariants

* `title` is required (1–200 chars)
* `completed` defaults to false
* `user_id` is immutable once set
* No cross‑user access under any circumstance

---

### 5. API Behavior Rules

* Requests without valid JWT → `401 Unauthorized`
* User ID in token **must match** URL user scope
* Errors return structured JSON
* CRUD operations are idempotent where applicable

---

### 6. Quality Gates (Phase II)

* All endpoints covered by specs
* Manual CRUD verification via UI
* Auth enforced on every route
* Database migrations reproducible

---

### 7. Phase II Exit Criteria

Phase II is complete when:

* A user can sign up and sign in
* Tasks persist across reloads
* One user cannot access another user's tasks
* All behavior matches approved specs

---

## Phase III – AI‑Powered Todo Chatbot Constitution

### 1. Purpose & Scope

Phase III introduces a **natural‑language chatbot** that manages todos using AI agents and MCP tools, without breaking Phase II guarantees.

**In Scope**

* Conversational task management
* MCP server & tools
* Conversation persistence
* Stateless AI request cycle

**Out of Scope**

* Kubernetes deployment
* Event‑driven Kafka features
* Voice input

---

### 2. Non‑Negotiable Principles

1. **Tools, Not Logic**
   AI agents may not directly manipulate the database; they must use MCP tools.
2. **Stateless Server**
   Each chat request is independent; state is reconstructed from DB.
3. **Deterministic Tool Contracts**
   MCP tools have strict schemas and predictable outputs.
4. **Human‑Readable Confirmation**
   Every action must be confirmed in natural language.
5. **No Spec Drift**
   Chatbot behavior must match existing task rules from Phase II.

---

### 3. Architecture Mandates

#### 3.1 Chat Flow

1. Receive user message
2. Load conversation history from DB
3. Run OpenAI Agent with MCP tools
4. Persist messages and tool calls
5. Return assistant response

#### 3.2 Components

* **Frontend**: OpenAI ChatKit UI
* **Backend**: FastAPI chat endpoint
* **AI Layer**: OpenAI Agents SDK
* **Integration**: Official MCP SDK

---

### 4. MCP Tool Constitution

#### Required Tools

* `add_task`
* `list_tasks`
* `update_task`
* `complete_task`
* `delete_task`

#### Tool Rules

* Must include `user_id`
* Must validate task ownership
* Must return structured JSON
* Must never expose raw DB errors

---

### 5. Agent Behavior Rules

* Infer intent from natural language
* Choose correct MCP tool(s)
* Chain tools when required (e.g., list → delete)
* Handle missing tasks gracefully
* Never hallucinate task IDs

---

### 6. Conversation & Data Rules

* Conversations are persisted
* Messages are immutable after creation
* Server memory holds no chat context
* Restarting server does not lose chat history

---

### 7. Security Constitution

* JWT authentication required for chat endpoint
* Agent only sees user‑scoped data
* MCP tools enforce ownership checks

---

### 8. Quality Gates (Phase III)

* Natural language CRUD verified
* Tool calls logged and auditable
* Conversations resumable after restart
* No direct DB access by agent

---

### 9. Phase III Exit Criteria

Phase III is complete when:

* Users manage tasks via natural language
* AI reliably maps intent to MCP tools
* Conversation state persists correctly
* All actions respect Phase II rules

---

## Constitutional Supremacy Clause

If any generated code conflicts with this Constitution, **the Constitution prevails**. Specs must be updated and code regenerated until compliance is achieved.

---

**End of Constitution – Phase II & Phase III**

## Response snapshot

Successfully updated the project constitution file at `.specify/memory/constitution.md` with the complete Todo App Constitution covering both Phase II (Full-Stack Web App) and Phase III (AI-Powered Chatbot). All placeholder tokens were replaced with concrete values from the provided content, maintaining proper formatting and structure. The constitution now serves as the authoritative document governing Spec-Driven Development for the Todo application.

## Outcome

- ✅ Impact: Updated project constitution with comprehensive guidelines for Todo App Phase II & III
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md, history/prompts/constitution/0001-update-todo-app-constitution.constitution.prompt.md
- 🔁 Next prompts: none
- 🧠 Reflection: Constitution serves as authoritative governance document ensuring consistent development practices across project phases

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): none needed