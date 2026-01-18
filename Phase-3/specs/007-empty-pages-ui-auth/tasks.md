# SP-EMPTY-PAGES-UI-AUTH – Execution Tasks

This **SP-TASKS** defines the **executable steps** for implementing **SP-EMPTY-PAGES-UI-AUTH** - Empty Pages, Professional Colors, Tailwind Enforcement & Auth Header Rules.

## Phase 1: Setup

### Goal
Initialize the environment and verify preconditions for the UI/UX improvements.

### Independent Test Criteria
- SP-EMPTY-PAGES-UI-AUTH specification is accessible
- Frontend structure is canonical
- Dev server can be stopped/restarted

### Tasks
- [x] T001 Verify SP-EMPTY-PAGES-UI-AUTH specification document exists at specs/007-empty-pages-ui-auth/spec.md
- [x] T002 Confirm canonical router path /frontend/src/app exists
- [x] T003 Verify forbidden path /frontend/app does NOT exist
- [x] T004 Stop any running dev servers before changes

## Phase 2: Foundational

### Goal
Prepare the foundation with Tailwind enforcement and color system.

### Independent Test Criteria
- Tailwind CSS is properly configured
- Color system is locked and consistent
- No inline styles or hex colors exist

### Tasks
- [x] T005 Verify globals.css contains ONLY Tailwind directives (@tailwind base, components, utilities)
- [x] T006 [P] Update tailwind.config.ts to include content: ['./src/**/*.{ts,tsx}']
- [x] T007 [P] Replace random color classes with semantic palette (bg-background, text-foreground, text-indigo-600, etc.)
- [x] T008 Remove all inline styles and hex colors from components

## Phase 3: Auth-Aware Layout [US1]

### Goal
Implement conditional header rendering based on route.

### Independent Test Criteria
- Header renders on main application routes
- Header is hidden on auth routes (/login, /signup)
- No duplicate header implementations exist

### Tasks
- [x] T009 [US1] Create header component at /frontend/src/components/header.tsx
- [x] T010 [US1] Implement route detection logic in header component
- [x] T011 [US1] Add conditional rendering to hide header on /login and /register routes
- [x] T012 [US1] Integrate header component into /frontend/src/app/layout.tsx

## Phase 4: Empty Page Content [US2]

### Goal
Eliminate blank pages with meaningful empty state content.

### Independent Test Criteria
- Dashboard page shows welcome content
- Tasks page shows "No tasks yet" with CTA when empty
- Chat page shows conversation prompt when empty

### Tasks
- [x] T013 [US2] Update home page (/frontend/src/app/page.tsx) with welcome message and app explanation
- [x] T014 [US2] Implement empty state for tasks page with icon, "No tasks yet" message and CTA button
- [x] T015 [US2] Create chat page at /frontend/src/app/chat/page.tsx with conversation prompt
- [x] T016 [US2] Add appropriate empty state icons and messages to all pages

## Phase 5: State Coverage [US3]

### Goal
Ensure all pages handle loading, empty, and error states properly.

### Independent Test Criteria
- Loading states render correctly
- Empty states are informative
- Error states use consistent styling
- No fake data is displayed

### Tasks
- [x] T017 [US3] Implement loading state handling on all pages
- [x] T018 [US3] Ensure error states use approved color classes (text-error, bg-background, border-border)
- [x] T019 [US3] Update login page to use approved color classes
- [x] T020 [US3] Update register page to use approved color classes

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Final validation and polish to ensure all requirements are met.

### Independent Test Criteria
- All SP-EMPTY-PAGES-UI-AUTH requirements are satisfied
- Implementation is stable and functional
- Tailwind utilities are visibly applied
- Colors are consistent across pages

### Tasks
- [x] T021 Verify Tailwind utilities are visibly applied across all pages
- [x] T022 Confirm professional color harmony is consistent throughout the application
- [x] T023 Validate header is hidden on auth routes (/login, /signup)
- [x] T024 Ensure all empty pages display informative content
- [x] T025 Confirm no inline styles exist anywhere in the UI
- [x] T026 Run final validation checklist against the specification
- [x] T027 Test all routes to verify proper header visibility/hidden state

## Dependencies

- Task T005 must complete before color system tasks
- Task T008 must complete before UI component updates
- Task T012 must complete before page content updates

## Parallel Execution Examples

- Tasks T006, T007 can run in parallel during foundational phase
- Tasks T019, T020 can run in parallel during state coverage
- Tasks T021, T022, T023, T024 can run in parallel during polish phase

## Implementation Strategy

1. **MVP First**: Complete Phase 1-2 to establish Tailwind and color foundation
2. **Incremental Delivery**: Complete auth-aware layout (Phase 3) as first deliverable
3. **Complete Implementation**: Finish empty page content (Phase 4) and state coverage (Phase 5)
4. **Final Polish**: Complete validation and cross-cutting concerns (Phase 6)