# Implementation Plan: Frontend UI for Todo Web Application

**Branch**: `001-frontend-ui` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-frontend-ui/spec.md`

## Summary

Build a complete, beautiful, and error-proof frontend web application for Phase II of the Hackathon Todo project. The frontend will provide authenticated users with a responsive interface to manage their personal todo tasks through CRUD operations. Implementation uses Next.js 15+ App Router with TypeScript and Tailwind CSS, integrating with Better Auth for authentication. The UI prioritizes user experience with comprehensive loading states, error handling, optimistic updates, and mobile-first responsive design. All task operations enforce user ownership through JWT-based authentication, aligning with constitutional principles.

**Technical Approach**: Modern React-based SPA using Next.js App Router for routing and server components where beneficial. Better Auth handles authentication flows and JWT management. Centralized API client (axios/fetch wrapper) manages all backend communication with automatic token attachment and error handling. Tailwind CSS provides utility-first styling with custom design tokens. State management uses React hooks (useState, useEffect, useContext) for local and shared state, avoiding unnecessary global state libraries. Optimistic UI updates provide instant feedback while API requests complete in background.

## Technical Context

**Language/Version**: TypeScript 5.3+, JavaScript ES2022+ (Next.js 15+ with React 19+)
**Primary Dependencies**:
- Next.js 15+ (App Router, React Server Components)
- React 19+
- Better Auth (frontend auth SDK)
- Tailwind CSS 3.4+
- Axios or native fetch for API client
- React Hook Form + Zod (form validation)
- Lucide React or Heroicons (iconography)

**Storage**: Browser localStorage for JWT token (with XSS mitigation) or httpOnly cookies if Better Auth provides cookie-based flow; no client-side database

**Testing**:
- Jest + React Testing Library (component unit tests)
- Playwright or Cypress (E2E tests for critical flows)
- TypeScript strict mode for compile-time safety

**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge - last 2 years), responsive design for desktop (>= 1024px), tablet (768-1023px), mobile (375px - 767px)

**Project Type**: Web application (frontend only; backend assumed to exist)

**Performance Goals**:
- Initial page load < 2 seconds on standard broadband
- Task operations (create, toggle, delete) feel instant (optimistic updates within 100ms)
- Lighthouse score: Performance > 90, Accessibility > 95, Best Practices > 95
- Bundle size: < 500KB initial load (gzipped)

**Constraints**:
- No backend implementation (frontend only)
- Must integrate with existing REST API endpoints (assumed to exist)
- Must enforce user ownership (JWT required on all task operations)
- Mobile-first responsive design (minimum 375px width)
- Accessibility WCAG AA minimum
- No Phase III features (chatbot, real-time sync, task sharing)

**Scale/Scope**:
- Support 100 tasks per user without performance degradation
- Single-user experience (no concurrent multi-tab sync required)
- Estimated 8-10 reusable components
- 4-5 pages/routes (landing, login, signup, dashboard, optional 404)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ Principle I: User Ownership (NON-NEGOTIABLE)**
- JWT token attached to ALL API requests automatically via API client interceptor
- No task operations possible without valid authentication
- Dashboard only displays user's own tasks (backend enforces with user_id filtering)
- Frontend never attempts to access other users' data

**✅ Principle II: REST API Contract**
- All API calls use standard REST methods: GET, POST, PUT/PATCH, DELETE
- API client targets `/api/*` endpoints only
- Expects JSON responses, parses accordingly
- Handles standard HTTP status codes (2xx, 4xx, 5xx)
- Implements retry logic for network failures, redirects to login on 401

**✅ Principle III: Authentication & Authorization**
- Better Auth manages JWT lifecycle (creation, storage, refresh, clearing)
- Token stored securely (localStorage with XSS mitigation or httpOnly cookie)
- Authorization header attached to every API request: `Authorization: Bearer <JWT>`
- 401 responses trigger logout and redirect to login page
- No hardcoded credentials, no auth bypasses

**✅ Principle IV: Phase Boundaries (STRICT)**
- In scope: Authentication UI, task dashboard, task CRUD, responsive design, error handling
- Out of scope: No chatbot features, no task sharing, no WebSocket sync, no admin panel
- No code or UI elements for Phase III features

**✅ Principle V: Database Schema Integrity**
- Frontend does not directly interact with database (backend responsibility)
- Respects API responses; assumes backend enforces user ownership and cascading deletes

**✅ Principle VI: Error Handling & Observability**
- All API errors captured and displayed with user-friendly messages
- Console logging for debugging (development mode)
- Toast notifications for transient errors
- Detailed error messages never expose stack traces or internal details

**✅ Principle VII: Simplicity & Pragmatism**
- No unnecessary abstractions; start with simple React hooks before adding global state
- Tailwind utility classes prevent CSS complexity
- Reusable components only when pattern repeats 3+ times
- No premature optimization; measure first

**Gate Status**: ✅ PASSED - All constitutional principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-frontend-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-client.md    # API client interface contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/                        # Next.js 15+ App Router
│   ├── (auth)/                 # Route group for auth pages (shared layout)
│   │   ├── login/
│   │   │   └── page.tsx        # Login page
│   │   ├── signup/
│   │   │   └── page.tsx        # Signup page
│   │   └── layout.tsx          # Auth layout (centered card, no navbar)
│   ├── (dashboard)/            # Route group for authenticated pages
│   │   ├── dashboard/
│   │   │   └── page.tsx        # Main dashboard with task list
│   │   └── layout.tsx          # Dashboard layout (with navbar, auth guard)
│   ├── layout.tsx              # Root layout (HTML, global styles, fonts)
│   ├── page.tsx                # Landing page (unauthenticated home)
│   └── globals.css             # Tailwind directives + custom CSS variables
├── components/                 # Reusable UI components
│   ├── auth/
│   │   ├── AuthForm.tsx        # Shared auth form component (login/signup)
│   │   ├── AuthGuard.tsx       # HOC to protect routes (redirect if unauthenticated)
│   │   └── LogoutButton.tsx    # Logout button with confirmation
│   ├── tasks/
│   │   ├── TaskCard.tsx        # Individual task item with checkbox, delete, edit
│   │   ├── TaskForm.tsx        # Create/edit task form (inline or modal)
│   │   ├── TaskList.tsx        # List container for tasks with empty state
│   │   └── TaskSkeleton.tsx    # Loading skeleton for task cards
│   ├── ui/
│   │   ├── Button.tsx          # Reusable button component (variants: primary, secondary, danger)
│   │   ├── Input.tsx           # Reusable input with label and error state
│   │   ├── Toast.tsx           # Toast notification component
│   │   └── Modal.tsx           # Modal/dialog component (optional for edit)
│   ├── Navbar.tsx              # Main navigation bar with logout
│   └── ErrorBoundary.tsx       # React error boundary for graceful failures
├── lib/                        # Utility functions and API client
│   ├── api/
│   │   ├── client.ts           # Axios/fetch wrapper with interceptors
│   │   ├── auth.ts             # Auth API calls (login, signup, logout)
│   │   └── tasks.ts            # Task API calls (CRUD operations)
│   ├── auth/
│   │   └── better-auth.ts      # Better Auth configuration and hooks
│   ├── hooks/
│   │   ├── useAuth.ts          # Custom hook for auth state and operations
│   │   ├── useTasks.ts         # Custom hook for task state and CRUD operations
│   │   └── useToast.ts         # Custom hook for toast notifications
│   ├── utils/
│   │   ├── cn.ts               # Tailwind class name merger (clsx + tailwind-merge)
│   │   └── validation.ts       # Zod schemas for form validation
│   └── types/
│       ├── auth.ts             # TypeScript types for auth (User, LoginCredentials, etc.)
│       └── task.ts             # TypeScript types for tasks (Task, CreateTaskInput, etc.)
├── public/                     # Static assets
│   ├── images/
│   │   └── empty-state.svg     # Empty state illustration for no tasks
│   └── favicon.ico
├── tests/                      # Test files
│   ├── e2e/
│   │   ├── auth.spec.ts        # E2E tests for auth flows
│   │   └── tasks.spec.ts       # E2E tests for task CRUD
│   └── components/
│       ├── TaskCard.test.tsx   # Unit tests for TaskCard
│       └── TaskForm.test.tsx   # Unit tests for TaskForm
├── .env.local                  # Environment variables (API base URL, etc.)
├── next.config.js              # Next.js configuration
├── tailwind.config.ts          # Tailwind configuration with custom theme
├── tsconfig.json               # TypeScript configuration
├── package.json                # Dependencies and scripts
└── README.md                   # Project setup and development instructions
```

**Structure Decision**:
Selected **Option 2: Web application** structure with frontend-only implementation (backend assumed to exist separately). Using Next.js 15+ App Router conventions with route groups for organization (`(auth)` for public pages, `(dashboard)` for protected pages). Component organization follows atomic design principles: `components/ui/` for primitive UI elements, `components/tasks/` for domain-specific components, `components/auth/` for authentication-related components. The `lib/` directory centralizes business logic, API integration, and shared utilities to keep components lean and focused on presentation.

## Complexity Tracking

> **No violations detected** - Constitution Check passed with no complexity justifications required.

---

## Phase 0: Research & Technology Decisions

**Objective**: Resolve all technical unknowns and validate technology choices before design phase.

### Research Tasks

1. **Better Auth Integration Pattern**
   - **Question**: How to integrate Better Auth with Next.js 15 App Router for JWT-based authentication?
   - **Research Focus**:
     - Better Auth React SDK installation and configuration
     - JWT storage strategy (localStorage vs httpOnly cookies)
     - Token refresh mechanism
     - Auth state persistence across page reloads
   - **Decision Criteria**: Simplicity, security, compatibility with Next.js App Router

2. **API Client Architecture**
   - **Question**: Should we use Axios, native fetch, or a library like TanStack Query for API calls?
   - **Research Focus**:
     - Interceptor support for automatic token attachment
     - Error handling and retry logic
     - TypeScript support and type inference
     - Bundle size impact
   - **Decision Criteria**: Developer experience, bundle size, error handling capabilities

3. **Form Validation Strategy**
   - **Question**: Best approach for client-side form validation (React Hook Form + Zod vs Formik vs native)?
   - **Research Focus**:
     - TypeScript integration and type safety
     - Error message customization
     - Performance with controlled inputs
     - Accessibility support
   - **Decision Criteria**: Type safety, DX, bundle size, accessibility

4. **State Management Approach**
   - **Question**: Do we need a global state library (Zustand, Redux, Jotai) or are React hooks sufficient?
   - **Research Focus**:
     - Auth state sharing across components
     - Task list state management
     - Optimistic updates pattern
   - **Decision Criteria**: Simplicity (constitution Principle VII), avoiding over-engineering

5. **Optimistic UI Update Pattern**
   - **Question**: How to implement optimistic updates for task operations (toggle, delete, create)?
   - **Research Focus**:
     - Rollback strategy on API failure
     - Preventing race conditions with rapid clicks
     - User feedback during optimistic state
   - **Decision Criteria**: User experience (instant feedback), reliability (correct rollback)

6. **Responsive Design Strategy**
   - **Question**: Mobile-first Tailwind approach vs separate mobile/desktop components?
   - **Research Focus**:
     - Tailwind breakpoint best practices
     - Container queries vs media queries
     - Touch-friendly interaction patterns (44px tap targets)
   - **Decision Criteria**: Maintainability, performance, design consistency

7. **Error Handling UI Patterns**
   - **Question**: Toast notifications vs inline errors vs error boundary pages?
   - **Research Focus**:
     - When to use each pattern (transient errors vs permanent failures)
     - Accessibility considerations (ARIA live regions for toasts)
     - User actions on errors (retry, dismiss, contact support)
   - **Decision Criteria**: Accessibility, user clarity, implementation complexity

8. **Loading State UI Patterns**
   - **Question**: Skeleton loaders vs spinners vs progress indicators?
   - **Research Focus**:
     - Skeleton UI best practices (mimicking final layout)
     - Spinner placement (inline vs overlay)
     - Perceived performance benefits
   - **Decision Criteria**: User experience, implementation effort, accessibility

### Research Deliverable

All research findings will be documented in `research.md` with:
- **Decision**: Technology/pattern chosen
- **Rationale**: Why this choice aligns with constitution and project goals
- **Alternatives Considered**: Other options evaluated and why rejected
- **Implementation Notes**: Key configuration or patterns to follow

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` completed with all technology choices finalized

### 1. Data Model (`data-model.md`)

**Frontend Data Models** (TypeScript interfaces):

#### User Entity
```typescript
interface User {
  id: string;           // UUID from backend
  email: string;        // User's email address
  createdAt: string;    // ISO 8601 timestamp
}
```

**Validation Rules**:
- Email must match standard email regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- ID is backend-generated, never modified client-side

**State Transitions**: User exists in auth context after successful login/signup, cleared on logout

---

#### Task Entity
```typescript
interface Task {
  id: string;           // UUID from backend
  title: string;        // Task description (max 255 chars)
  completed: boolean;   // Completion status
  userId: string;       // Owner's user ID (for reference, not exposed in UI)
  createdAt: string;    // ISO 8601 timestamp
  updatedAt: string;    // ISO 8601 timestamp
}
```

**Validation Rules**:
- Title: 1-255 characters, non-empty, trimmed whitespace
- Completed: boolean only (no null/undefined)
- Timestamps: ISO 8601 format, backend-controlled

**State Transitions**:
- `completed: false` → `completed: true` (toggle complete)
- `completed: true` → `completed: false` (toggle incomplete)
- Task can be edited (title updated) in either state
- Task can be deleted in either state

---

#### Auth State
```typescript
interface AuthState {
  user: User | null;         // Current authenticated user or null
  token: string | null;      // JWT token or null
  isAuthenticated: boolean;  // Derived from token existence
  isLoading: boolean;        // Auth initialization in progress
}
```

**State Transitions**:
1. Initial: `{ user: null, token: null, isAuthenticated: false, isLoading: true }`
2. After auth check: `isLoading: false`, others updated based on stored token
3. After login/signup: `{ user: User, token: string, isAuthenticated: true, isLoading: false }`
4. After logout: `{ user: null, token: null, isAuthenticated: false, isLoading: false }`

---

#### Form Inputs
```typescript
interface LoginCredentials {
  email: string;
  password: string;
}

interface SignupCredentials {
  email: string;
  password: string;
  confirmPassword: string;  // Client-side only validation
}

interface CreateTaskInput {
  title: string;
}

interface UpdateTaskInput {
  title: string;
}
```

**Validation Rules** (Zod schemas):
- LoginCredentials: email format + password min 8 chars
- SignupCredentials: email format + password min 8 chars + passwords match
- CreateTaskInput: title 1-255 chars, trimmed
- UpdateTaskInput: title 1-255 chars, trimmed

---

### 2. API Contracts (`contracts/api-client.md`)

**API Client Interface Specification**

#### Base Configuration
- **Base URL**: Configurable via environment variable `NEXT_PUBLIC_API_BASE_URL` (e.g., `http://localhost:8000`)
- **Default Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>` (auto-attached if token exists)
- **Timeout**: 30 seconds for all requests
- **Retry Policy**: Retry on network errors (max 2 retries with exponential backoff), no retry on 4xx errors

#### Authentication Endpoints

**POST `/api/auth/signup`**
- **Request Body**: `{ email: string, password: string }`
- **Response (201)**: `{ user: User, token: string }`
- **Errors**:
  - `400`: `{ error: string, code: "VALIDATION_ERROR", details: object }`
  - `409`: `{ error: string, code: "EMAIL_EXISTS" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**POST `/api/auth/login`**
- **Request Body**: `{ email: string, password: string }`
- **Response (200)**: `{ user: User, token: string }`
- **Errors**:
  - `400`: `{ error: string, code: "VALIDATION_ERROR" }`
  - `401`: `{ error: string, code: "INVALID_CREDENTIALS" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**POST `/api/auth/logout`** (optional, depends on backend)
- **Request Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{ message: "Logged out successfully" }`
- **Errors**:
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`

---

#### Task Endpoints

**GET `/api/tasks`**
- **Request Headers**: `Authorization: Bearer <token>`
- **Query Params**: None (pagination out of scope for Phase II)
- **Response (200)**: `{ tasks: Task[] }`
- **Errors**:
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**POST `/api/tasks`**
- **Request Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{ title: string }`
- **Response (201)**: `{ task: Task }`
- **Errors**:
  - `400`: `{ error: string, code: "VALIDATION_ERROR", details: object }`
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**GET `/api/tasks/:id`** (optional, may not be needed if list fetch provides all)
- **Request Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{ task: Task }`
- **Errors**:
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`
  - `403`: `{ error: string, code: "FORBIDDEN" }` (task belongs to another user)
  - `404`: `{ error: string, code: "NOT_FOUND" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**PATCH `/api/tasks/:id`**
- **Request Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{ title: string }`
- **Response (200)**: `{ task: Task }`
- **Errors**:
  - `400`: `{ error: string, code: "VALIDATION_ERROR", details: object }`
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`
  - `403`: `{ error: string, code: "FORBIDDEN" }`
  - `404`: `{ error: string, code: "NOT_FOUND" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**PATCH `/api/tasks/:id/toggle`**
- **Request Headers**: `Authorization: Bearer <token>`
- **Request Body**: None (or `{}`)
- **Response (200)**: `{ task: Task }` (with `completed` toggled)
- **Errors**:
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`
  - `403`: `{ error: string, code: "FORBIDDEN" }`
  - `404`: `{ error: string, code: "NOT_FOUND" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

**DELETE `/api/tasks/:id`**
- **Request Headers**: `Authorization: Bearer <token>`
- **Response (204)**: No content (or `200` with `{ message: "Task deleted" }`)
- **Errors**:
  - `401`: `{ error: string, code: "UNAUTHORIZED" }`
  - `403`: `{ error: string, code: "FORBIDDEN" }`
  - `404`: `{ error: string, code: "NOT_FOUND" }`
  - `500`: `{ error: string, code: "SERVER_ERROR" }`

---

#### Error Handling Contract

**Client-Side Error Mapping**:
- `400 VALIDATION_ERROR` → Display specific field errors from `details` object
- `401 UNAUTHORIZED` → Clear auth state, redirect to `/login` with message "Session expired, please log in again"
- `403 FORBIDDEN` → Display toast: "You don't have permission to perform this action"
- `404 NOT_FOUND` → Display toast: "Resource not found" (or handle gracefully by removing from UI)
- `409 EMAIL_EXISTS` → Display inline error: "An account with this email already exists"
- `500 SERVER_ERROR` → Display toast: "Something went wrong. Please try again later."
- Network errors (timeout, no connection) → Display toast: "Network error. Please check your connection."

**User-Friendly Message Mapping**:
```typescript
const ERROR_MESSAGES: Record<string, string> = {
  VALIDATION_ERROR: "Please check your input and try again.",
  INVALID_CREDENTIALS: "Invalid email or password.",
  EMAIL_EXISTS: "An account with this email already exists.",
  UNAUTHORIZED: "Your session has expired. Please log in again.",
  FORBIDDEN: "You don't have permission to perform this action.",
  NOT_FOUND: "The requested resource was not found.",
  SERVER_ERROR: "Something went wrong. Please try again later.",
  NETWORK_ERROR: "Network error. Please check your connection and try again.",
};
```

---

### 3. Quickstart Guide (`quickstart.md`)

**Developer Setup and Running the Frontend**

#### Prerequisites
- Node.js 18+ and npm 9+ (or yarn/pnpm)
- Backend API running and accessible (assumed)
- Git for version control

#### Initial Setup
```bash
# Clone the repository (if not already cloned)
cd "D:/Hackathon II (Todo App)/Phase 2 (Todo Full Stack)"

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables template
cp .env.local.example .env.local

# Edit .env.local to set API base URL
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

#### Development Server
```bash
# Run development server
npm run dev

# Open browser to http://localhost:3000
# App will hot-reload on file changes
```

#### Building for Production
```bash
# Create optimized production build
npm run build

# Start production server
npm start
```

#### Running Tests
```bash
# Run all unit tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run E2E tests (requires app to be running)
npm run test:e2e
```

#### Code Quality
```bash
# Run ESLint
npm run lint

# Fix auto-fixable linting issues
npm run lint:fix

# Format code with Prettier
npm run format

# Type-check with TypeScript
npm run type-check
```

#### Project Structure Overview
- `/app` - Next.js pages and layouts (App Router)
- `/components` - Reusable React components
- `/lib` - API client, utilities, hooks, types
- `/public` - Static assets
- `/tests` - Test files

#### Key Environment Variables
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL (e.g., `http://localhost:8000`)
- `NEXT_PUBLIC_APP_NAME` - App name for branding (optional, default: "Hackathon Todo")

#### Common Development Tasks
- **Add a new component**: Create in `/components/<category>/ComponentName.tsx`
- **Add a new page**: Create in `/app/<route>/page.tsx`
- **Add an API function**: Create in `/lib/api/<domain>.ts`
- **Add a custom hook**: Create in `/lib/hooks/useHookName.ts`
- **Update styles**: Modify Tailwind config in `tailwind.config.ts` or add to `app/globals.css`

---

### 4. Agent Context Update

**Run agent context update script** (if applicable):
```bash
.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude
```

This updates the Claude-specific agent context file with:
- Technology stack: Next.js 15+, React 19+, TypeScript, Tailwind CSS, Better Auth
- Project structure: App Router with route groups
- Key patterns: Optimistic updates, centralized API client, custom hooks
- Testing approach: Jest + React Testing Library, Playwright/Cypress

**Manual additions preserved** between markers in agent context file.

---

## Post-Phase 1 Constitution Re-Check

**Re-evaluating against constitutional principles after design decisions:**

**✅ Principle I: User Ownership** - API client automatically attaches JWT to all requests; no manual token management in components reduces error risk.

**✅ Principle II: REST API Contract** - API contracts documented with exact endpoints, methods, and response formats matching backend specification.

**✅ Principle III: Authentication & Authorization** - Better Auth chosen for robust JWT management; 401/403 handling redirects to login automatically.

**✅ Principle IV: Phase Boundaries** - Data model and API contracts strictly limited to Phase II features (no sharing, no chatbot, no admin).

**✅ Principle V: Database Schema Integrity** - Frontend respects backend-provided data shapes; no client-side schema assumptions beyond API contracts.

**✅ Principle VI: Error Handling & Observability** - Comprehensive error mapping defined with user-friendly messages; no stack traces exposed.

**✅ Principle VII: Simplicity & Pragmatism** - Technology choices prioritize simplicity: React hooks over Redux, Tailwind over CSS-in-JS, fetch/axios over complex query libraries (unless TanStack Query adds significant value with minimal complexity).

**Gate Status**: ✅ PASSED - Design aligns with all constitutional principles.

---

## Next Steps

1. **Complete Phase 0**: Fill `research.md` with technology decisions (Better Auth integration, API client choice, form library, state management approach, UI patterns).

2. **Complete Phase 1**: Create `data-model.md`, `contracts/api-client.md`, and `quickstart.md` as specified above.

3. **Run `/sp.tasks`**: Generate actionable implementation tasks from this plan, breaking down into atomic units for development.

4. **Begin Implementation**: Follow tasks in priority order (P1 first), starting with project setup and authentication before task management features.

---

## Notes

- This plan focuses on **frontend implementation only**; backend API is assumed to exist and conform to documented contracts.
- Better Auth integration details depend on research findings; may require adjustments if SDK does not support App Router cleanly.
- Optimistic UI updates are critical for user experience but add complexity to error handling; research phase must validate feasibility.
- Mobile-first approach means desktop layouts are enhancements, not the baseline; all components must work at 375px width first.
- Accessibility is non-negotiable (WCAG AA minimum); use semantic HTML, ARIA labels, keyboard navigation from the start.
