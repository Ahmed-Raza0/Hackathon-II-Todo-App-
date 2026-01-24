---
id: 1
title: Backend Frontend Integration Plan
stage: plan
date_iso: 2026-01-20
surface: agent
model: qwen-2.5-72b-instruct
feature: 005-backend-frontend-integration
branch: 005-backend-frontend-integration
user: Claude
command: sp.plan
labels: ["integration", "backend", "frontend", "auth", "cors", "api", "authentication"]
links:
  spec: /mnt/d/Hackathon II (Todo App)/Phase-3/specs/005-backend-frontend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-backend-frontend-integration/plan.md
  - specs/005-backend-frontend-integration/research.md
  - specs/005-backend-frontend-integration/data-model.md
  - specs/005-backend-frontend-integration/quickstart.md
  - specs/005-backend-frontend-integration/contracts/auth-contract.md
  - specs/005-backend-frontend-integration/contracts/tasks-contract.md
  - history/prompts/005-backend-frontend-integration/001-backend-frontend-integration-plan.plan.prompt.md
tests: []
---

# Backend Frontend Integration Plan

## Summary

Created comprehensive implementation plan for backend-frontend integration and error resolution. This includes:

1. Implementation plan outlining technical context and architecture
2. Research document detailing technology decisions and patterns
3. Data model defining entities and API contracts
4. API contracts for authentication and task management endpoints
5. Quickstart guide for setting up and running the integrated application

The plan addresses all requirements from the feature specification, including proper CORS configuration, JWT authentication flow, API contract compliance, and error handling to ensure seamless frontend-backend communication.

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

Successfully completed the implementation plan for the backend-frontend integration feature. The plan includes:

1. **Technical Context**: Defined the technology stack (Python 3.11+, Next.js 16+, Neon PostgreSQL, SQLModel, etc.)
2. **Constitution Check**: Verified all requirements from the project constitution are met
3. **Project Structure**: Outlined the complete directory structure for both backend and frontend
4. **Research**: Created comprehensive research document covering technology decisions and architecture patterns
5. **Data Model**: Defined the entities needed for the integration (User Session, API Request)
6. **API Contracts**: Created detailed contracts for both authentication and task management endpoints
7. **Quickstart Guide**: Provided setup and testing instructions

All artifacts are properly organized in the feature directory and ready for the next phase of task generation. The plan follows all constitution requirements and is fully aligned with the feature specification.

## Outcome

The implementation plan is complete and ready for the next phase (`/sp.tasks`). All necessary design artifacts have been created including research, data model, API contracts, and quickstart guide. The frontend and backend integration components are properly specified with clear API contracts and authentication flow requirements.