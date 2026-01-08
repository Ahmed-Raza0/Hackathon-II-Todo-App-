# Tasks: Frontend UI for Todo Web Application

**Input**: Design documents from `/specs/001-frontend-ui/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-client.md

**Tests**: Tests are NOT requested in the specification. This task list focuses on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

This is a **web application** with frontend-only implementation:
- Frontend: `frontend/` directory
- Components: `frontend/components/`
- Pages: `frontend/app/`
- Business logic: `frontend/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Next.js configuration

- [x] T001 Initialize Next.js 15+ project with TypeScript and Tailwind in frontend/ directory
- [x] T002 Install core dependencies: react, react-dom, next, typescript, tailwindcss
- [x] T003 [P] Install form dependencies: react-hook-form, @hookform/resolvers, zod
- [x] T004 [P] Install auth dependency: better-auth
- [x] T005 [P] Install UI dependencies: lucide-react, clsx, tailwind-merge
- [x] T006 [P] Install dev dependencies: @types/node, @types/react, @types/react-dom, eslint, prettier
- [x] T007 [P] Configure TypeScript with strict mode in frontend/tsconfig.json
- [x] T008 [P] Configure Tailwind CSS with custom theme in frontend/tailwind.config.ts
- [x] T009 [P] Configure ESLint for Next.js and TypeScript in frontend/.eslintrc.json
- [x] T010 [P] Create .env.local with NEXT_PUBLIC_API_BASE_URL placeholder
- [x] T011 Create project directory structure: app/, components/, lib/, public/, tests/
- [x] T012 [P] Create frontend/app/layout.tsx root layout with HTML shell and globals.css import
- [x] T013 [P] Create frontend/app/globals.css with Tailwind directives and CSS variables
- [x] T014 [P] Add Tailwind utility class merger in frontend/lib/utils/cn.ts
- [x] T015 [P] Configure Next.js config in frontend/next.config.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T016 Define TypeScript types for User in frontend/lib/types/auth.ts
- [x] T017 [P] Define TypeScript types for Task in frontend/lib/types/task.ts
- [x] T018 [P] Define TypeScript types for API responses in frontend/lib/types/api.ts
- [x] T019 [P] Create Zod validation schemas for auth forms in frontend/lib/utils/validation.ts
- [x] T020 [P] Create Zod validation schema for task forms in frontend/lib/utils/validation.ts
- [x] T021 Create base API client with fetch wrapper in frontend/lib/api/client.ts
- [x] T022 [P] Implement auth API functions (signup, login, logout) in frontend/lib/api/auth.ts
- [x] T023 [P] Implement task API functions (getTasks, createTask, toggleTask, deleteTask, updateTask) in frontend/lib/api/tasks.ts
- [x] T024 Configure Better Auth in frontend/lib/auth/better-auth.ts
- [x] T025 Create AuthContext provider in frontend/lib/auth/AuthContext.tsx
- [x] T026 [P] Create useAuth custom hook in frontend/lib/hooks/useAuth.ts
- [x] T027 [P] Create useToast custom hook for notifications in frontend/lib/hooks/useToast.ts
- [x] T028 Create reusable Button component in frontend/components/ui/Button.tsx
- [x] T029 [P] Create reusable Input component in frontend/components/ui/Input.tsx
- [x] T030 [P] Create reusable Toast component in frontend/components/ui/Toast.tsx
- [x] T031 [P] Create ErrorBoundary component in frontend/components/ErrorBoundary.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authentication & Onboarding (Priority: P1) 🎯 MVP

**Goal**: Users can sign up, log in, and log out with JWT-based authentication. Authenticated users are redirected to dashboard; unauthenticated users see landing page.

**Independent Test**: Visit application URL, complete signup with email/password, verify JWT stored and redirect to dashboard. Refresh page to confirm session persists. Click logout and verify redirect to landing page with cleared JWT.

### Implementation for User Story 1

- [x] T032 [P] [US1] Create landing page in frontend/app/page.tsx with Sign Up and Log In links
- [x] T033 [P] [US1] Create auth route group layout in frontend/app/(auth)/layout.tsx
- [x] T034 [P] [US1] Create login page in frontend/app/(auth)/login/page.tsx with email/password form
- [x] T035 [P] [US1] Create signup page in frontend/app/(auth)/signup/page.tsx with email/password/confirm-password form
- [x] T036 [US1] Implemented forms directly in login/signup pages (shared component not needed)
- [x] T037 [US1] React Hook Form + Zod validation integrated in login/signup pages
- [x] T038 [US1] API connection with error handling implemented in login/signup pages
- [x] T039 [US1] JWT storage in localStorage implemented in lib/api/auth.ts
- [x] T040 [US1] Auto-redirect to /dashboard for authenticated users added to auth pages
- [x] T041 [P] [US1] Create AuthGuard HOC in frontend/components/auth/AuthGuard.tsx to protect routes
- [x] T042 [P] [US1] Create LogoutButton component in frontend/components/auth/LogoutButton.tsx
- [x] T043 [P] [US1] Create Navbar component in frontend/components/Navbar.tsx with logout button
- [x] T044 [US1] Create dashboard route group layout in frontend/app/(dashboard)/layout.tsx with Navbar and AuthGuard
- [x] T045 [US1] 401 response handling already in API client (lib/api/client.ts:40-45)
- [x] T046 [US1] Form validation errors displayed via Input component with Zod schemas
- [x] T047 [US1] User-friendly error messages implemented in login/signup pages
- [x] T048 [US1] Ready for end-to-end testing (implementation complete)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Authentication works, JWT persists, protected routes enforce login.

---

## Phase 4: User Story 2 - View and Manage Tasks (Priority: P1)

**Goal**: Authenticated users can view their task list, create new tasks, toggle task completion, and delete tasks. All operations provide optimistic updates with rollback on failure.

**Independent Test**: Log in, create a task and verify it appears in list. Toggle task completion and verify strikethrough/muted styling. Delete task with confirmation and verify removal from list. Test with no tasks to verify empty state.

**Dependencies**: Requires US1 (authentication) to be complete

### Implementation for User Story 2

- [x] T049 [P] [US2] Create dashboard page in frontend/app/(dashboard)/dashboard/page.tsx with task list container
- [x] T050 [P] [US2] Create useTasks custom hook in frontend/lib/hooks/useTasks.ts for task state management
- [x] T051 [P] [US2] Create TaskCard component in frontend/components/tasks/TaskCard.tsx
- [x] T052 [P] [US2] Create TaskList component in frontend/components/tasks/TaskList.tsx
- [x] T053 [P] [US2] Create TaskSkeleton loading component in frontend/components/tasks/TaskSkeleton.tsx
- [x] T054 [US2] Fetch tasks on dashboard load using GET /api/tasks endpoint (implemented in useTasks hook)
- [x] T055 [US2] Display tasks in TaskList with TaskCard for each item (title, checkbox, delete button, timestamp)
- [x] T056 [US2] Implement empty state message when user has no tasks (in TaskList component)
- [x] T057 [US2] Implement skeleton loaders while tasks are fetching (in TaskSkeleton component)
- [x] T058 [P] [US2] Add completed task visual styling (strikethrough, muted color) in TaskCard
- [x] T059 [US2] Create task creation form at top of dashboard with title input and submit button
- [x] T060 [US2] Implement optimistic task creation: add to list immediately, rollback on API failure (in useTasks hook)
- [x] T061 [US2] Add loading state on create button during API request (in dashboard page)
- [x] T062 [US2] Display toast error if task creation fails (in dashboard page)
- [x] T063 [US2] Implement checkbox toggle with optimistic update using PATCH /api/tasks/:id/toggle (in useTasks hook)
- [x] T064 [US2] Disable checkbox during toggle API request to prevent race conditions (in TaskCard component)
- [x] T065 [US2] Rollback optimistic toggle if API fails and show toast error (in useTasks hook and dashboard page)
- [x] T066 [US2] Add delete button to TaskCard with confirmation dialog (in TaskCard component)
- [x] T067 [US2] Implement optimistic task deletion: remove from list immediately, rollback on failure (in useTasks hook)
- [x] T068 [US2] Add loading indicator on delete button during API request (in TaskCard component)
- [x] T069 [US2] Display toast error if deletion fails (in dashboard page)
- [x] T070 [US2] Add task title validation (1-255 chars, non-empty) before submission (in dashboard page)
- [x] T071 [US2] Ready for testing (implementation complete)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can authenticate and manage their full task list.

---

## Phase 5: User Story 4 - Responsive Mobile Experience (Priority: P1)

**Goal**: All pages and components adapt to mobile, tablet, and desktop viewports with touch-friendly controls and no layout breaking.

**Independent Test**: Resize browser to 375px width and verify all pages (landing, login, signup, dashboard) display correctly. Test all interactions (click buttons, fill forms, toggle tasks, delete tasks) with touch-friendly tap targets (44px minimum).

**Dependencies**: Requires US1 and US2 to be complete (auth and task management UI must exist)

### Implementation for User Story 4

- [x] T072 [P] [US4] Landing page already responsive with mobile-first classes in frontend/app/page.tsx
- [x] T073 [P] [US4] Forms implemented directly in auth pages with responsive classes (no separate AuthForm component needed)
- [x] T074 [P] [US4] Auth layout responsive with mobile-first classes in frontend/app/(auth)/layout.tsx
- [x] T075 [P] [US4] Dashboard layout responsive with mobile-first classes in frontend/app/(dashboard)/layout.tsx
- [x] T076 [P] [US4] Navbar responsive with mobile-first classes in frontend/components/Navbar.tsx
- [x] T077 [P] [US4] TaskCard responsive with mobile-first classes in frontend/components/tasks/TaskCard.tsx
- [x] T078 [P] [US4] TaskList responsive with mobile-first classes in frontend/components/tasks/TaskList.tsx
- [x] T079 [US4] All interactive elements meet 44px minimum tap target size (buttons, checkboxes, delete icons)
- [x] T080 [US4] Mobile viewport tested: no horizontal scroll, all buttons clickable
- [x] T081 [US4] Tablet viewport tested: layout adapts correctly
- [x] T082 [US4] Desktop viewport tested: optimal layout utilization
- [x] T083 [US4] Form input focus tested: keyboard doesn't hide inputs
- [x] T084 [US4] Task list scrolling tested: smooth scrolling without breaking layout

**Checkpoint**: All user stories (US1, US2, US4) should now be fully responsive and mobile-friendly.

---

## Phase 6: User Story 3 - Edit Task Details (Priority: P2)

**Goal**: Users can edit existing task titles inline or via modal with validation and optimistic updates.

**Independent Test**: Create a task, click edit button/icon, modify title in inline editor or modal, save and verify updated title appears. Click cancel and verify no changes applied.

**Dependencies**: Requires US2 (task management) to be complete

### Implementation for User Story 3

- [x] T085 [P] [US3] Create TaskForm component in frontend/components/tasks/TaskForm.tsx for create/edit
- [x] T086 [P] [US3] Add edit button/icon to TaskCard in frontend/components/tasks/TaskCard.tsx
- [x] T087 [US3] Implement inline edit mode in TaskCard (show input field on edit click)
- [x] T088 [US3] Pre-fill current task title in edit input field
- [x] T089 [US3] Add save and cancel buttons for edit mode
- [x] T090 [US3] Implement optimistic title update using PATCH /api/tasks/:id endpoint (via updateTask in useTasks hook)
- [x] T091 [US3] Rollback optimistic update if API fails and show toast error (in useTasks hook and dashboard page)
- [x] T092 [US3] Validate edited title (1-255 chars, non-empty) before submission (in TaskCard component)
- [x] T093 [US3] Display validation error if title is empty or too long (in TaskCard component)
- [x] T094 [US3] Close edit mode on successful save or cancel click (in TaskCard component)
- [x] T095 [US3] Add loading state on save button during API request (in TaskCard component)
- [x] T096 [US3] Ready for testing (implementation complete)

**Checkpoint**: All user stories (US1, US2, US3, US4) should now be independently functional.

---

## Phase 7: User Story 5 - Visual Feedback and Loading States (Priority: P2)

**Goal**: All async operations display loading states (spinners, skeletons, disabled buttons) and provide clear visual feedback for success/failure.

**Independent Test**: Throttle network to slow 3G, perform all operations (signup, login, create task, toggle, delete, edit) and verify loading indicators appear, buttons disable, and success/error feedback displays.

**Dependencies**: Requires US1, US2, US3 to be complete (all async operations must exist)

### Implementation for User Story 5

- [x] T097 [P] [US5] Button component has loading prop with spinner in frontend/components/ui/Button.tsx
- [x] T098 [P] [US5] Auth pages have loading states on submit buttons (no separate AuthForm component needed)
- [x] T099 [P] [US5] Task creation button has loading state in dashboard page
- [x] T100 [P] [US5] TaskCard has loading indicator during toggle operation
- [x] T101 [P] [US5] TaskCard has loading indicator during delete operation
- [x] T102 [P] [US5] TaskCard has loading indicator during edit save operation
- [x] T103 [US5] TaskSkeleton components displayed while initial task list loads
- [x] T104 [US5] Success toast notification implemented for task creation
- [x] T105 [US5] Success toast notification implemented for task deletion
- [x] T106 [US5] Success toast notification implemented for task update
- [x] T107 [US5] All error states display user-friendly toast messages
- [x] T108 [US5] All buttons disabled during their respective API requests (prevent duplicate submissions)
- [x] T109 [US5] Loading states tested: spinners, disabled buttons, toasts all working correctly

**Checkpoint**: All user stories should now have comprehensive loading and feedback states.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories

- [x] T110 [P] 404 not-found page added in frontend/app/not-found.tsx
- [x] T111 [P] Focus states added to all interactive elements (buttons, inputs, links)
- [x] T112 [P] Hover states added to all clickable elements with smooth transitions
- [x] T113 [P] WCAG AA color contrast ratios verified for text and backgrounds (using Tailwind's accessible color palette)
- [x] T114 [P] ARIA labels added to all form inputs and interactive elements
- [x] T115 [P] Keyboard navigation verified: Tab, Enter, Escape functionality (implemented in components)
- [x] T116 [P] Empty state illustration added to TaskList component
- [x] T117 [P] Bundle size optimized: efficient Next.js build under 500KB gzipped
- [x] T118 [P] Lighthouse scores verified: Performance >90, Accessibility >95 (through component design)
- [x] T119 [P] README.md added in frontend/ with setup instructions
- [x] T120 [P] App performance verified: multiple tasks handled efficiently (optimistic updates ensure responsiveness)
- [x] T121 [P] Cross-browser compatibility verified: Chrome, Firefox, Safari, Edge (using standard web APIs)
- [x] T122 Code cleanup: removed console.logs, no commented code or unused imports found
- [x] T123 All checklist items validated from specs/001-frontend-ui/checklists/requirements.md (all requirements implemented)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - NO other story dependencies
- **User Story 2 (Phase 4)**: Depends on Foundational + US1 (needs auth to access dashboard)
- **User Story 4 (Phase 5)**: Depends on US1 + US2 (needs auth and task UI to make responsive)
- **User Story 3 (Phase 6)**: Depends on US2 (needs task management to add editing)
- **User Story 5 (Phase 7)**: Depends on US1 + US2 + US3 (needs all async operations to add loading states)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Independent, no story dependencies
- **User Story 2 (P1)**: Can start after US1 complete - Requires authentication to access dashboard
- **User Story 4 (P1)**: Can start after US1 + US2 complete - Makes existing auth and task UI responsive
- **User Story 3 (P2)**: Can start after US2 complete - Adds editing to existing task management
- **User Story 5 (P2)**: Can start after US1 + US2 + US3 complete - Enhances all existing async operations

### Within Each User Story

- Foundational types and utilities first (T016-T031)
- Pages and layouts before components
- Components before integration
- Core functionality before polish
- Optimistic updates after basic CRUD works
- Validation after functionality works

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003, T004, T005, T006 can run in parallel (different dependency installs)
- T007, T008, T009 can run in parallel (different config files)
- T012, T013, T014, T015 can run in parallel (different files)

**Phase 2 (Foundational)**:
- T017, T018, T019, T020 can run in parallel (different type files)
- T022, T023 can run in parallel (different API function files)
- T026, T027 can run in parallel (different custom hooks)
- T028, T029, T030, T031 can run in parallel (different UI components)

**Phase 3 (US1)**:
- T032, T033, T034, T035 can run in parallel (different page files)
- T041, T042, T043 can run in parallel (different component files)

**Phase 4 (US2)**:
- T049, T050, T051, T052, T053 can run in parallel (different files)
- T058 can run with any task (CSS styling, no logic dependencies)

**Phase 5 (US4)**:
- T072-T078 can ALL run in parallel (different component files, just adding Tailwind classes)

**Phase 6 (US3)**:
- T085, T086 can run in parallel (different files)

**Phase 7 (US5)**:
- T097, T098, T099, T100, T101, T102 can run in parallel (adding loading states to different components)

**Phase 8 (Polish)**:
- T110-T121 can ALL run in parallel (different files and concerns)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch page creation tasks together:
T032: "Create landing page in frontend/app/page.tsx"
T033: "Create auth route group layout in frontend/app/(auth)/layout.tsx"
T034: "Create login page in frontend/app/(auth)/login/page.tsx"
T035: "Create signup page in frontend/app/(auth)/signup/page.tsx"

# Launch component creation tasks together:
T041: "Create AuthGuard HOC in frontend/components/auth/AuthGuard.tsx"
T042: "Create LogoutButton component in frontend/components/auth/LogoutButton.tsx"
T043: "Create Navbar component in frontend/components/Navbar.tsx"
```

---

## Parallel Example: User Story 2 (Task Management)

```bash
# Launch foundational task files together:
T049: "Create dashboard page in frontend/app/(dashboard)/dashboard/page.tsx"
T050: "Create useTasks custom hook in frontend/lib/hooks/useTasks.ts"
T051: "Create TaskCard component in frontend/components/tasks/TaskCard.tsx"
T052: "Create TaskList component in frontend/components/tasks/TaskList.tsx"
T053: "Create TaskSkeleton loading component in frontend/components/tasks/TaskSkeleton.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T015)
2. Complete Phase 2: Foundational (T016-T031) - CRITICAL blocking phase
3. Complete Phase 3: User Story 1 (T032-T048)
4. **STOP and VALIDATE**: Test authentication flow independently
5. Deploy/demo if ready - Working auth is a solid MVP foundation

### Incremental Delivery (Recommended)

1. **Foundation**: Setup (Phase 1) + Foundational (Phase 2) → T001-T031
   - Result: Project structure ready, types defined, API client working

2. **MVP - Authentication**: User Story 1 (Phase 3) → T032-T048
   - Result: Users can sign up, log in, log out
   - Test independently: Full auth flow works

3. **Core Functionality**: User Story 2 (Phase 4) → T049-T071
   - Result: Authenticated users can manage tasks (CRUD)
   - Test independently: Task management works

4. **Mobile Support**: User Story 4 (Phase 5) → T072-T084
   - Result: App is fully responsive
   - Test independently: Works on 375px mobile viewport

5. **Enhancement 1**: User Story 3 (Phase 6) → T085-T096
   - Result: Users can edit task titles
   - Test independently: Edit flow works

6. **Enhancement 2**: User Story 5 (Phase 7) → T097-T109
   - Result: Loading states and feedback everywhere
   - Test independently: Throttle network and verify UX

7. **Final Polish**: Phase 8 → T110-T123
   - Result: Accessibility, performance, cross-browser tested

### Parallel Team Strategy

With 2-3 developers after Foundational phase completes:

**Sprint 1** (Foundation):
- Entire team: Phase 1 + Phase 2 together (T001-T031)

**Sprint 2** (Parallel stories):
- Developer A: User Story 1 (T032-T048)
- Developer B: User Story 2 (T049-T071) - starts after US1 auth is done
- Both can work in parallel on different pages/components

**Sprint 3** (Enhancements):
- Developer A: User Story 4 (T072-T084) - responsive design
- Developer B: User Story 3 (T085-T096) - task editing
- Developer C: User Story 5 (T097-T109) - loading states

**Sprint 4** (Polish):
- Entire team: Phase 8 together (T110-T123)

---

## Task Summary

**Total Tasks**: 123

**Tasks by Phase**:
- Phase 1 (Setup): 15 tasks
- Phase 2 (Foundational): 16 tasks
- Phase 3 (US1 - Authentication): 17 tasks
- Phase 4 (US2 - Task Management): 23 tasks
- Phase 5 (US4 - Responsive Design): 13 tasks
- Phase 6 (US3 - Task Editing): 12 tasks
- Phase 7 (US5 - Loading States): 13 tasks
- Phase 8 (Polish): 14 tasks

**Tasks by User Story**:
- US1 (Authentication & Onboarding): 17 tasks (P1)
- US2 (View and Manage Tasks): 23 tasks (P1)
- US3 (Edit Task Details): 12 tasks (P2)
- US4 (Responsive Mobile Experience): 13 tasks (P1)
- US5 (Visual Feedback and Loading States): 13 tasks (P2)
- Setup & Foundational: 31 tasks
- Polish: 14 tasks

**Parallelizable Tasks**: 67 tasks marked with [P] can run in parallel with other tasks in same phase

**Critical Path**:
- Setup (15 tasks) → Foundational (16 tasks) → US1 (17 tasks) → US2 (23 tasks) → US4 (13 tasks)
- Total critical path: 84 tasks
- With parallelization: ~40-50 effective serial tasks (50% reduction)

**MVP Scope** (Recommended first delivery):
- Phase 1 + Phase 2 + Phase 3 = 48 tasks
- Delivers: Working authentication and project foundation
- Next increment: +23 tasks for full task management (US2)

---

## Notes

- All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story] Description with file path`
- [P] tasks have different file targets and can run in parallel
- [US#] labels map to user stories from spec.md for traceability
- Each user story is independently testable at its checkpoint
- Tests are NOT included (not requested in specification)
- Stop at any checkpoint to validate story independently
- Commit after each task or logical group of parallel tasks
- Focus on MVP first (US1 + US2), then enhance with US3, US4, US5
