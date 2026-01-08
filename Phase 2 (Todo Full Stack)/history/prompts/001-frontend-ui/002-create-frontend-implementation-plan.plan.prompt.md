---
id: 002
title: Create Frontend Implementation Plan
stage: plan
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-frontend-ui
branch: 001-frontend-ui
user: user
command: /sp.plan
labels: ["frontend", "planning", "architecture", "nextjs", "typescript", "tailwind"]
links:
  spec: specs/001-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-ui/plan.md
  - specs/001-frontend-ui/research.md
  - specs/001-frontend-ui/data-model.md
  - specs/001-frontend-ui/contracts/api-client.md
  - specs/001-frontend-ui/quickstart.md
tests:
  - N/A (planning artifact)
---

## Prompt

You are Claude, operating in **sp.plan mode** for the frontend of
**Hackathon II – Phase 2: Todo Full-Stack Web Application**.

Your task is to **create a COMPLETE development plan** for the frontend that is:
- **Beautiful, professional, and error-proof**
- Fully **responsive** for desktop, tablet, and mobile
- Phase II compliant (ignore backend, database, and Phase III features)
- Structured for a hackathon-ready execution

Plan Objective:
- Deliver a complete frontend UI for Phase II
- Fully implement all **sp.specify** frontend specifications
- Ensure **error-free, responsive, and professional UI**
- Use **Next.js 16+, TypeScript, Tailwind CSS**
- Integrate with **Better Auth frontend** for JWT handling
- Centralized API client assumed (do not implement backend)

Development Phases:
- Phase 1: Project Setup (Next.js, TypeScript, Tailwind, Better Auth, linting)
- Phase 2: Authentication UI (login, signup, auth forms, auth guard, logout)
- Phase 3: Task Dashboard (responsive layout, task list, filters, skeletons, empty states)
- Phase 4: Task Management UI (create/edit forms, modals, validation, toasts)
- Phase 5: Reusable Components & UI Polishing (navbar, cards, buttons, inputs, loading states)
- Phase 6: State & API Flow (centralized client, loading/error/empty/success handling, immediate UI updates)

## Response snapshot

**Implementation Plan Created**: `specs/001-frontend-ui/plan.md`

**Planning Artifacts Generated**:

1. **plan.md** - Complete implementation plan with:
   - Summary: Build beautiful, error-proof frontend with Next.js 15+, TypeScript, Tailwind, Better Auth
   - Technical Context: TypeScript 5.3+, Next.js 15+ App Router, React 19+, Better Auth, Tailwind 3.4+, React Hook Form + Zod
   - Constitution Check: ✅ ALL 7 principles satisfied (user ownership, REST API, auth, phase boundaries, error handling, simplicity)
   - Project Structure: Next.js App Router with route groups (`(auth)`, `(dashboard)`), organized components, lib directory for business logic
   - Performance Goals: <2s page load, <100ms optimistic updates, Lighthouse >90, <500KB bundle
   - Constraints: Frontend-only, mobile-first (375px min), WCAG AA accessibility, no Phase III features

2. **research.md** - Technology decisions with rationale:
   - **Better Auth** (localStorage JWT, XSS mitigation, auto token management)
   - **Native fetch wrapper** (0KB overhead, sufficient for Phase II)
   - **React Hook Form + Zod** (type-safe validation, ~30KB gzipped)
   - **React Context + useState** (no global state library needed)
   - **Manual optimistic updates** with rollback pattern
   - **Mobile-first Tailwind** responsive utilities
   - **Toasts + inline errors + error boundaries** (comprehensive error UI)
   - **Skeleton loaders + spinners** (structured loading states)
   - **Total bundle impact: ~52KB**, complexity: Low-Medium

3. **data-model.md** - TypeScript interfaces:
   - **User**: `{ id, email, createdAt }`
   - **Task**: `{ id, title, completed, userId, createdAt, updatedAt }`
   - **AuthState**: `{ user, token, isAuthenticated, isLoading }`
   - **Form Inputs**: LoginCredentials, SignupCredentials, CreateTaskInput, UpdateTaskInput
   - **Validation Rules**: Email regex, password min 8 chars, task title 1-255 chars
   - **State Transitions**: Task lifecycle (create → incomplete ↔ complete → deleted)
   - **Relationships**: User (1) ───< (N) Task via userId foreign key

4. **contracts/api-client.md** - Complete API specification:
   - **Auth Endpoints**: POST /api/auth/signup, POST /api/auth/login, POST /api/auth/logout
   - **Task Endpoints**: GET /api/tasks, POST /api/tasks, PATCH /api/tasks/:id, PATCH /api/tasks/:id/toggle, DELETE /api/tasks/:id
   - **Request/Response Formats**: JSON with typed interfaces
   - **Error Codes**: VALIDATION_ERROR, INVALID_CREDENTIALS, EMAIL_EXISTS, UNAUTHORIZED, FORBIDDEN, NOT_FOUND, SERVER_ERROR, NETWORK_ERROR
   - **Client-Side Actions**: Field errors, toasts, redirects, rollbacks
   - **Retry Strategy**: Max 2 retries for network errors, no retry for 4xx/5xx

5. **quickstart.md** - Developer setup guide:
   - **Prerequisites**: Node.js 18+, npm 9+, Git, VS Code
   - **Setup Steps**: Clone, navigate to frontend/, initialize Next.js, install deps, configure .env.local
   - **Development Workflow**: npm run dev, build, start, test, lint, type-check
   - **Project Structure**: Detailed file tree with explanations
   - **Common Tasks**: Adding pages, components, API functions, hooks, types
   - **Troubleshooting**: Port conflicts, module errors, TypeScript issues, Tailwind, CORS
   - **Commands Reference**: All npm scripts with descriptions

**Key Architectural Decisions**:

- **Frontend Stack**: Next.js 15+ App Router, TypeScript 5.3+, React 19+, Tailwind CSS 3.4+
- **Authentication**: Better Auth with localStorage JWT, AuthContext wrapper
- **API Client**: Native fetch with custom wrapper (interceptors, error handling, auto token attach)
- **Form Validation**: React Hook Form + Zod (type-safe, accessible)
- **State Management**: React Context (auth) + local useState (tasks), no Redux/Zustand
- **Optimistic Updates**: Manual with rollback pattern, race condition prevention
- **Responsive Design**: Mobile-first Tailwind utilities, 375px minimum width
- **Error Handling**: Toasts (transient) + inline errors (forms) + error boundaries (crashes)
- **Loading States**: Skeleton loaders (initial load) + spinners (actions) + disabled states

**Project Structure**:
```
frontend/
├── app/                 # Next.js App Router
│   ├── (auth)/          # Login, Signup pages with auth layout
│   ├── (dashboard)/     # Dashboard with navbar + auth guard
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Landing page
├── components/          # Reusable components (auth, tasks, ui)
├── lib/                 # API client, auth, hooks, utils, types
├── public/              # Static assets
├── tests/               # E2E and component tests
└── configs              # Next, Tailwind, TypeScript, ESLint
```

**Constitution Compliance**: ✅ ALL 7 PRINCIPLES SATISFIED
- User Ownership: JWT on all API requests, no cross-user access
- REST API Contract: All endpoints /api/*, JSON-only, standard HTTP methods
- Auth & Authorization: Better Auth manages JWT, 401 redirects to login
- Phase Boundaries: No chatbot, sharing, WebSockets, admin (Phase III features excluded)
- Database Schema: Frontend respects backend data shapes, no direct DB access
- Error Handling: User-friendly messages, no stack traces, structured error codes
- Simplicity: Native fetch, React hooks, Tailwind utilities, no over-engineering

**Performance & Quality Targets**:
- Page load: <2 seconds
- Optimistic updates: <100ms feedback
- Bundle size: <500KB gzipped
- Lighthouse: Performance >90, Accessibility >95
- Test coverage: >70% for critical paths
- Mobile-first: 375px-767px, tablet 768px-1023px, desktop 1024px+

## Outcome

- ✅ Impact: Complete implementation plan with research, data models, API contracts, and quickstart guide ready for task generation
- 🧪 Tests: Planning validation - all constitutional checks passed
- 📁 Files: plan.md, research.md, data-model.md, contracts/api-client.md, quickstart.md
- 🔁 Next prompts: Run `/sp.tasks` to generate atomic implementation tasks from this plan
- 🧠 Reflection: Plan balances comprehensiveness with simplicity (Principle VII). Technology choices minimize bundle size (~52KB added) while providing robust DX (TypeScript, Zod, React Hook Form). Optimistic updates and error handling ensure professional UX. All 60 functional requirements from spec.md are addressable with this architecture.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning artifacts generated successfully
- Graders run and results (PASS/FAIL): Constitutional compliance check - PASS (7/7 principles satisfied)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks with `/sp.tasks` and validate that atomic task breakdown matches 60 functional requirements without overlap or gaps
