---
id: 1
title: Create Fullstack Todo App Plan
stage: plan
date_iso: 2026-01-19
surface: agent
model: qwen-2.5-72b-instruct
feature: 002-fullstack-todo-app
branch: 002-fullstack-todo-app
user: Claude
command: sp.plan
labels: ["plan", "fullstack", "todo-app", "architecture", "database", "api"]
links:
  spec: /mnt/d/Hackathon II (Todo App)/specs/002-fullstack-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-todo-app/plan.md
  - specs/002-fullstack-todo-app/research.md
  - specs/002-fullstack-todo-app/data-model.md
  - specs/002-fullstack-todo-app/quickstart.md
  - specs/002-fullstack-todo-app/contracts/api-contract.md
  - CLAUDE.md
  - history/prompts/002-fullstack-todo-app/001-create-fullstack-todo-app-plan.plan.prompt.md
tests: []
---

# Create Fullstack Todo App Plan

## Summary

Created a comprehensive implementation plan for the Full-Stack Todo Application, including research, data model, API contracts, and quickstart guide. The plan follows the constitution requirements and prepares for the next phase of task generation.

## Prompt Text

```
# Hackathon II Todo App - sp.plan.md

**Purpose:** Define the exact order of implementation tasks for Phase II (Full-Stack Web App) and Phase III (AI Chatbot).
All tasks must follow this plan; no skipping allowed. References: `sp.specify.md`, `sp.constitution.md`.

---

## 1️⃣ Phase II - Full-Stack Web Application

### 1.1 Database Setup
1. Create `users` table (managed by Better Auth)
2. Create `tasks` table:
   - Columns: id, user_id, title, description, completed, created_at, updated_at
   - Indexes: user_id, completed
3. Configure `.env` with `DATABASE_URL`

---

### 1.2 Backend Setup
1. Initialize FastAPI app (`main.py`)
2. Create `db.py` / `database.py`:
   - Load `.env`
   - Create SQLModel engine
3. Create `models.py` for `Task` model
4. Implement JWT verification middleware
   - Verify JWT
   - Extract user_id
   - Attach to request context
5. Create `routes/` folder
   - Task CRUD endpoints
   - Route handlers must enforce ownership
6. Add error handling (401, 404, 400)
7. Ensure all routes under `/api/`

---

### 1.3 Frontend Setup
1. Next.js 16+ with App Router
2. Create `lib/api.ts` API client
   - Attach JWT token to all requests
3. Integrate Better Auth signup/login
4. Create `/app/tasks` page
   - List tasks (filtered by logged-in user)
   - Create, update, delete, toggle complete
5. Tailwind CSS styling
6. Ensure all requests include JWT header

---

### 1.4 Integration & Verification
1. Test JWT auth end-to-end
2. Test Task CRUD endpoints
3. Verify user isolation
4. Verify database persistence in Neon PostgreSQL
5. Document working endpoints in `sp.specify.md`

---

## 2️⃣ Phase III - AI Chatbot

### 2.1 Database
1. Create `conversations` table:
   - Columns: id, user_id, created_at, updated_at
2. Create `messages` table:
   - Columns: id, user_id, conversation_id, role, content, created_at
3. Add foreign keys and indexes

---

### 2.2 Backend: MCP & Agent
1. Setup MCP server
2. Implement MCP tools:
   - `add_task`, `list_tasks`, `complete_task`, `update_task`, `delete_task`
3. Implement chat endpoint (`/api/{user_id}/chat`)
   - Receive message
   - Fetch conversation history
   - Run OpenAI Agent with MCP tools
   - Store user message + assistant response in DB
   - Return response + tool_calls
4. Ensure stateless backend

---

### 2.3 Frontend: ChatKit Integration
1. Create ChatKit UI
2. Connect to `/api/{user_id}/chat`
3. Display conversation history
4. Stream AI responses
5. Include error handling for invalid requests

---

### 2.4 Testing & Validation
1. Validate all CRUD operations through AI commands:
   - "Add task…", "Show all tasks", "Complete task…", etc.
2. Verify task ownership enforcement
3. Confirm AI assistant responds correctly and uses MCP tools
4. Validate conversation persistence in DB
5. Confirm JWT auth enforced on chat endpoint

---

## 3️⃣ General Rules
- Follow **sp.constitution.md** strictly
- Always reference relevant specs: `@specs/features/task-crud.md`, `@specs/features/authentication.md`, `@specs/features/chatbot.md`
- No implementation without spec reference
- Phase III only starts after Phase II CRUD + Auth is fully working
- Task completion in Claude Code must follow order defined here

---

**Bottom Line:**
This plan ensures **safe, spec-driven, phased development**, starting from **database → backend → frontend → AI → chat integration**, fully aligned with monorepo structure, authentication, and stateless design principles.
```

## Response Text

Completed the implementation plan for the Full-Stack Todo Application with the following deliverables:

1. **Implementation Plan** (`plan.md`): Comprehensive plan with technical context, constitution check, and project structure
2. **Research Document** (`research.md`): Resolved all technical unknowns including language choices, dependencies, and constraints
3. **Data Model** (`data-model.md`): Detailed entity definitions with attributes, relationships, and validation rules
4. **API Contracts** (`contracts/api-contract.md`): Complete API specification with endpoints, request/response formats, and error handling
5. **Quickstart Guide** (`quickstart.md`): Step-by-step setup instructions for developers
6. **Agent Context Update**: Updated CLAUDE.md with relevant technology stack information

The plan follows all constitution requirements including security, user isolation, stateless architecture, layered responsibility, and technology stack compliance. All artifacts are created and the project is ready for the next phase of task generation.

## Outcome

Successfully created a complete implementation plan that satisfies all requirements from the feature specification and constitution. The plan includes all necessary design documents to proceed with task generation and implementation.