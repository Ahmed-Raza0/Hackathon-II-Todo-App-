# Feature Specification: Frontend App Router Path Resolution

**Feature Branch**: `003-fix-frontend-app-router-path`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "# Frontend App Router Path Specification (SP-SRC)

This **SP-SPECIFY** resolves ambiguity when a Next.js frontend contains **both**:

* `/frontend/app`
* `/frontend/src/app`

Only **one canonical App Router path** is permitted. This spec is binding.

---

## SP-SRC-01: Purpose

* Eliminate routing conflicts
* Prevent 404 errors caused by dual app directories
* Lock a single source of truth for the App Router

---

## SP-SRC-02: Canonical Rule (Non-Negotiable)

**Exactly ONE of the following may exist:**

* ✅ `/frontend/app`  **OR**
* ✅ `/frontend/src/app`

**Both existing simultaneously is FORBIDDEN.**

---

## SP-SRC-03: Approved Standard (Phase III)

For this project, the **canonical and approved structure** is:

```
/frontend
 ├── src/
 │   ├── app/              ← CANONICAL
 │   │   ├── layout.tsx
 │   │   ├── page.tsx
 │   │   └── globals.css
 │   └── lib/
 ├── tailwind.config.ts
 ├── next.config.js
 └── package.json
```

---

## SP-SRC-04: Forbidden Structures

❌ Forbidden:

```
/frontend/app
/frontend/src/app
```

❌ Forbidden:

```
/frontend/app/page.tsx
/frontend/src/app/page.tsx
```

Reason: Next.js cannot deterministically resolve the router.

---

## SP-SRC-05: Enforcement Actions

If `/frontend/app` exists:

1. DELETE `/frontend/app`
2. Ensure `/frontend/src/app` exists
3. Restart dev server

Manual patching inside components is NOT allowed.

---

## SP-SRC-06: page.tsx Invariant

```
/frontend/src/app/page.tsx
```

* MUST exist
* MUST export default component
* Missing file → guaranteed 404

---

## SP-SRC-07: layout.tsx Invariant

```
/frontend/src/app/layout.tsx
```

* MUST exist
* MUST wrap `{children}`

---

## SP-SRC-08: Validation Rules

After enforcement:

```
npm run dev
```

Then:

```
http://localhost:3000
```

Expected:

* Home page renders
* No 404

---

## SP-SRC-09: Supremacy Clause

This SP-SRC overrides all previous frontend folder assumptions.

If conflict occurs:

**SP-SRC > SP-FIX > SP-PLAN**

---

**End of Frontend App Router Path Specification (SP-SRC)**"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - App Router Resolution (Priority: P1)

As a developer, I want the Next.js app to have a single canonical App Router path so that I don't encounter routing conflicts or 404 errors due to dual app directories.

**Why this priority**: This is the foundational issue that must be resolved before any other frontend development can proceed reliably.

**Independent Test**: Can be fully tested by running `npm run dev` and navigating to the root URL, verifying the app renders without 404 errors. This delivers the core value of having a functional, predictable frontend routing system.

**Acceptance Scenarios**:

1. **Given** I have a Next.js project with potentially conflicting app directory structures, **When** I run `npm run dev`, **Then** the development server starts without router conflicts and serves the home page at http://localhost:3000.
2. **Given** The app is running correctly, **When** I navigate to the root URL, **Then** I see the home page without 404 errors.

---

### User Story 2 - Development Workflow (Priority: P2)

As a developer, I want to follow a standardized project structure so that I know exactly where to place my Next.js App Router files.

**Why this priority**: This ensures consistent development practices and prevents future conflicts.

**Independent Test**: Can be tested by verifying the correct directory structure exists and following the SP-SRC-03 standard. This delivers the value of predictable development patterns.

**Acceptance Scenarios**:

1. **Given** I'm adding new pages to the application, **When** I create a new route, **Then** I place the files in `/frontend/src/app/` following the canonical structure.
2. **Given** I need to modify the root layout, **When** I edit the layout file, **Then** I modify `/frontend/src/app/layout.tsx`.

---

### User Story 3 - Deployment Consistency (Priority: P3)

As a deployer, I want the app router structure to be consistent so that deployments work predictably without routing errors.

**Why this priority**: This ensures production deployments work reliably.

**Independent Test**: Can be tested by building the application and verifying the build succeeds without router conflicts. This delivers the value of reliable production deployments.

**Acceptance Scenarios**:

1. **Given** I'm preparing for deployment, **When** I run `npm run build`, **Then** the build completes successfully without router conflicts.
2. **Given** The application is deployed, **When** users access the site, **Then** all routes resolve correctly without 404 errors.

---

### Edge Cases

- What happens when both `/frontend/app` and `/frontend/src/app` exist simultaneously?
- How does the system handle migration from the forbidden structure to the canonical structure?
- What occurs when the canonical structure is missing required files (page.tsx, layout.tsx)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST enforce only one App Router directory structure exists at a time (either `/frontend/app` OR `/frontend/src/app`)
- **FR-002**: System MUST follow the canonical structure with app directory under `/frontend/src/app/`
- **FR-003**: Application MUST render the home page at the root route without 404 errors
- **FR-004**: Layout component MUST wrap all child routes in the application
- **FR-005**: All Next.js App Router features MUST function correctly with the canonical structure
- **FR-006**: Development server MUST start without router resolution conflicts
- **FR-007**: Production build MUST complete successfully with the canonical structure
- **FR-008**: Page component MUST be the default export in `/frontend/src/app/page.tsx`

### Key Entities *(include if feature involves data)*

- **App Router Structure**: The canonical directory structure for Next.js App Router components at `/frontend/src/app/`
- **Layout Component**: The root layout that wraps all child components in the application
- **Page Component**: The default page component that renders at the root route

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Development server starts successfully with no router conflicts
- **SC-002**: Home page renders at http://localhost:3000 without 404 errors
- **SC-003**: Only one App Router directory structure exists (either `/frontend/app` OR `/frontend/src/app`)
- **SC-004**: All routes resolve correctly in both development and production builds
- **SC-005**: Next.js App Router features work as expected with the canonical structure