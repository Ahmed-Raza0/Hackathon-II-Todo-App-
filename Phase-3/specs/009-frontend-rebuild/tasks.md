# SP-FRONTEND-REBUILD – Execution Tasks (Frontend ↔ Backend Add Integration)

This **SP-TASKS** defines the **executable steps** for implementing the **SP-FRONTEND-REBUILD** specification to ensure proper Tailwind CSS loading and UI quality.

## Phase 1: Setup

### Goal
Initialize the environment and verify preconditions for the frontend rebuild.

### Independent Test Criteria
- SP-FRONTEND-REBUILD specification is accessible
- Node.js and npm are available
- Development server can be stopped/restarted

### Tasks
- [x] T001 Verify SP-FRONTEND-REBUILD specification document exists at specs/009-frontend-rebuild/spec.md
- [x] T002 Confirm Node.js and npm are available in the environment
- [x] T003 Verify development server can be stopped and restarted

## Phase 2: Foundational

### Goal
Prepare the foundation with required CSS configuration files and project structure.

### Independent Test Criteria
- Global CSS file exists with required Tailwind directives
- Tailwind configuration has correct content paths
- PostCSS configuration is properly set up
- Project structure follows canonical pattern

### Tasks
- [x] T004 [P] Create/verify global CSS file exists at /frontend/src/app/globals.css
- [x] T005 [P] Ensure globals.css contains only required Tailwind directives (@tailwind base/components/utilities)
- [x] T006 [P] Verify layout.tsx imports globals.css at the top of the file
- [x] T007 [P] Update tailwind.config.ts with correct content paths: './src/**/*.{ts,tsx}'
- [x] T008 [P] Create/verify postcss.config.js with proper Tailwind and Autoprefixer configuration

## Phase 3: Project Structure [US1]

### Goal
Establish the canonical frontend structure as specified.

### Independent Test Criteria
- All required directories exist (app, components, lib)
- No forbidden directories exist (pages, nested frontend)
- Structure matches the canonical specification

### Tasks
- [x] T009 [US1] Create app directory structure: /frontend/src/app/{tasks,chat,login,signup}
- [x] T010 [US1] Create components directory: /frontend/src/components
- [x] T011 [US1] Create lib directory: /frontend/src/lib
- [x] T012 [US1] Remove any forbidden directories (pages/, nested frontend/)

## Phase 4: Core Page Implementation [US2]

### Goal
Create all required pages with meaningful content to prevent empty routes.

### Independent Test Criteria
- Dashboard page renders with welcome content
- Tasks page renders with empty state and form
- Chat page renders with intro message
- Login/Signup pages render without header

### Tasks
- [x] T013 [US2] Create dashboard page at /frontend/src/app/page.tsx with welcome content
- [x] T014 [US2] Create tasks page at /frontend/src/app/tasks/page.tsx with empty state and form
- [x] T015 [US2] Create chat page at /frontend/src/app/chat/page.tsx with intro message
- [x] T016 [US2] Create login page at /frontend/src/app/login/page.tsx without header
- [x] T017 [US2] Create signup page at /frontend/src/app/signup/page.tsx without header

## Phase 5: Navigation & Header [US3]

### Goal
Implement navigation and header with proper visibility rules.

### Independent Test Criteria
- Header component exists and functions properly
- Header shows on main routes, hides on auth routes
- Navigation works between all pages

### Tasks
- [x] T018 [US3] Create Header component at /frontend/src/components/Header.tsx
- [x] T019 [US3] Implement conditional header visibility based on route
- [x] T020 [US3] Add navigation links using next/link
- [x] T021 [US3] Test navigation functionality between all pages

## Phase 6: API Integration [US4]

### Goal
Set up backend integration with proper authentication.

### Independent Test Criteria
- API client exists and functions correctly
- JWT tokens are attached to requests
- Backend calls succeed with proper authentication

### Tasks
- [x] T022 [US4] Create API client at /frontend/src/lib/api.ts
- [x] T023 [US4] Implement JWT token attachment in API requests
- [x] T024 [US4] Add error handling for API responses
- [x] T025 [US4] Test API integration with backend endpoints

## Phase 7: UI Quality & Validation [US5]

### Goal
Ensure professional appearance and proper functionality.

### Independent Test Criteria
- All pages have proper Tailwind styling
- UI follows professional design standards
- All functionality works as expected

### Tasks
- [x] T026 [US5] Apply consistent spacing and typography across all pages
- [x] T027 [US5] Ensure no inline styles exist in components
- [x] T028 [US5] Verify responsive design works correctly
- [x] T029 [US5] Test all interactive elements have proper states
- [x] T030 [US5] Validate all pages load with proper styling

## Phase 8: Final Validation & Polish

### Goal
Final validation and ensure all requirements are met.

### Independent Test Criteria
- All SP-FRONTEND-REBUILD requirements are satisfied
- Implementation is stable and functional
- No CSS import violations remain
- Tailwind classes render correctly on 100% of pages

### Tasks
- [x] T031 Verify all Tailwind utility classes render correctly on all pages
- [x] T032 Confirm no inline styles or custom CSS exists in components
- [x] T033 Validate all pages load with proper styling
- [x] T034 Ensure no CSS import violations exist in pages/components
- [x] T035 Perform final validation that UI appears professionally styled
- [x] T036 Update documentation to reflect the CSS enforcement implementation
- [x] T037 Create summary report of the frontend rebuild process

## Dependencies

- Task T004 must complete before CSS import verification tasks
- Task T008 must complete before server restart validation
- All configuration tasks must complete before validation phase

## Parallel Execution Examples

- Tasks T004, T005, T006, T007, T008 can run in parallel during foundational phase
- Tasks T013, T014, T015, T016, T017 can run in parallel during page creation
- Tasks T026, T027, T028, T029, T30 can run in parallel during UI quality phase

## Implementation Strategy

1. **MVP First**: Complete Phase 1-2 to establish proper CSS configuration and project structure
2. **Incremental Delivery**: Complete page creation (Phase 4) as first deliverable
3. **Complete Implementation**: Finish navigation (Phase 5) and API integration (Phase 6)
4. **Final Polish**: Complete UI quality and validation (Phases 7-8)