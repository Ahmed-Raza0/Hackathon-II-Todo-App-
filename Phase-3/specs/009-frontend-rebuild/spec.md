# SP-FRONTEND-REBUILD – Full Frontend Rebuild Specification (Authoritative)

This **SP-SPECIFY** defines the **complete, clean, from-scratch frontend rebuild** after deletion. It exists to permanently eliminate:

• Broken navigation
• CSS / Tailwind not loading
• Header not routing correctly
• Frontend ↔ backend integration failure

This spec is **binding** and must be followed exactly. No improvisation.

## SP-FR-01: Scope & Intent

This rebuild will:

✔ Recreate frontend from ZERO
✔ Enforce correct App Router usage
✔ Guarantee Tailwind CSS works
✔ Ensure backend APIs work in frontend
✔ Align with Phase III Constitution & PDF

## SP-FR-02: Canonical Frontend Root (Non‑Negotiable)

```
/frontend
```

❌ Nested frontend folders are FORBIDDEN
❌ `/frontend/frontend` is FORBIDDEN

## SP-FR-03: Canonical Folder Structure (LOCKED)

```
/frontend
 ├── src
 │   ├── app
 │   │   ├── layout.tsx
 │   │   ├── page.tsx            # Dashboard
 │   │   ├── tasks
 │   │   │   └── page.tsx
 │   │   ├── chat
 │   │   │   └── page.tsx
 │   │   ├── login
 │   │   │   └── page.tsx
 │   │   ├── signup
 │   │   │   └── page.tsx
 │   │   └── globals.css
 │   ├── components
 │   │   ├── Header.tsx
 │   │   └── EmptyState.tsx
 │   ├── lib
 │   │   └── api.ts
 │   └── styles (FORBIDDEN)
 ├── tailwind.config.ts
 ├── postcss.config.js
 ├── next.config.js
 └── package.json
```

## SP-FR-04: Next.js Version Rule

• Next.js **13+** with App Router
• `pages/` directory is FORBIDDEN

## SP-FR-05: Tailwind CSS Enforcement (CRITICAL)

### globals.css (Exact)

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### layout.tsx MUST import

```ts
import './globals.css'
```

### tailwind.config.ts

```ts
content: ['./src/**/*.{ts,tsx}']
```

If CSS fails → frontend INVALID.

## SP-FR-06: Layout & Header Contract

### layout.tsx Responsibilities

• Import globals.css
• Wrap all pages
• Conditionally render Header

### Header Visibility Rules

| Route   | Header |
| ------- | ------ |
| /       | SHOW   |
| /tasks  | SHOW   |
| /chat   | SHOW   |
| /login  | HIDE   |
| /signup | HIDE   |

## SP-FR-07: Header & Navigation Specification

### Header.tsx MUST include

• App name
• Nav links (Dashboard, Tasks, Chat)
• Auth action (Login / Logout)

Navigation MUST use `next/link`.

## SP-FR-08: Page Content Rules (No Empty Pages)

### Dashboard (/)

• Welcome heading
• Short description

### Tasks (/tasks)

• Empty state
• Add task form
• Task list

### Chat (/chat)

• Intro message
• Chat input placeholder

### Login / Signup

• Proper form UI
• No Header

## SP-FR-09: Backend Integration Contract

### API Client

```
/frontend/src/lib/api.ts
```

All requests MUST:

• Use fetch
• Attach JWT token
• Handle errors

## SP-FR-10: Professional UI Rules

• Tailwind utilities only
• Consistent spacing
• Semantic colors only
• No inline styles

## SP-FR-11: Forbidden Patterns

❌ CSS files outside globals.css
❌ Header inside page files
❌ Hardcoded fake data
❌ Multiple App Routers

## SP-FR-12: Validation Checklist

✔ Tailwind visibly applied
✔ Navigation works
✔ Header hides on auth pages
✔ Backend calls succeed
✔ No 404 pages

## SP-FR-13: Supremacy Clause

Hierarchy:

**Constitution > PDF Spec > SP-FRONTEND-REBUILD > All Code**

If conflict occurs → regenerate frontend.

---

## User Scenarios & Testing

### Scenario 1: User Navigates to Dashboard
**Given**: User visits the root URL
**When**: User accesses the dashboard page
**Then**: User sees a welcome message and app description
**Validation**: Dashboard page loads with proper styling and header visible

### Scenario 2: User Navigates to Tasks Page
**Given**: User is authenticated and visits /tasks
**When**: User views the tasks page
**Then**: User sees empty state, add task form, and task list
**Validation**: Tasks page loads with proper styling and header visible

### Scenario 3: User Navigates to Chat Page
**Given**: User visits /chat
**When**: User views the chat page
**Then**: User sees intro message and chat input placeholder
**Validation**: Chat page loads with proper styling and header visible

### Scenario 4: User Accesses Login Page
**Given**: User visits /login
**When**: User views the login page
**Then**: User sees proper form UI without header
**Validation**: Login page loads without header and with proper styling

### Scenario 5: User Accesses Signup Page
**Given**: User visits /signup
**When**: User views the signup page
**Then**: User sees proper form UI without header
**Validation**: Signup page loads without header and with proper styling

## Functional Requirements

### FR-01: App Router Structure
**Requirement**: The system shall use Next.js App Router structure exclusively.
**Acceptance Criteria**:
- All pages are in the `/src/app` directory
- `pages/` directory does not exist
- Routes are properly defined with the correct file structure

### FR-02: Tailwind CSS Integration
**Requirement**: The system shall properly load and apply Tailwind CSS.
**Acceptance Criteria**:
- globals.css contains only the required Tailwind directives
- layout.tsx imports globals.css
- tailwind.config.ts has correct content paths
- All UI elements use Tailwind utility classes

### FR-03: Header Visibility Control
**Requirement**: The system shall conditionally display the header based on route.
**Acceptance Criteria**:
- Header is visible on main routes (/, /tasks, /chat)
- Header is hidden on auth routes (/login, /signup)
- Header component is implemented separately and conditionally rendered

### FR-04: Backend Integration
**Requirement**: The system shall properly integrate with backend APIs.
**Acceptance Criteria**:
- API client exists at `/frontend/src/lib/api.ts`
- All requests use proper authentication (JWT tokens)
- Error handling is implemented for all API calls

### FR-05: Page Content Standards
**Requirement**: All pages shall have meaningful content with no empty states.
**Acceptance Criteria**:
- Dashboard shows welcome content
- Tasks page shows empty state and add form
- Chat page shows intro message
- Auth pages show proper forms without header

## Success Criteria

### Quantitative Measures
- 100% of pages load with proper Tailwind styling
- 100% of routes follow the header visibility rules
- 100% of API calls properly attach JWT tokens
- 0% of CSS files exist outside globals.css
- 0% of inline styles used in components

### Qualitative Measures
- Navigation works smoothly between all pages
- UI appears professional with consistent spacing and colors
- All interactive elements have proper hover/focus states
- Backend integration functions properly without errors
- No 404 pages exist in the application

## Key Entities

### Layout Component
- **Location**: `/frontend/src/app/layout.tsx`
- **Purpose**: Root layout that wraps all pages
- **Responsibilities**: Import globals.css, conditionally render Header

### Header Component
- **Location**: `/frontend/src/components/Header.tsx`
- **Purpose**: Navigation component for main pages
- **Visibility**: Hidden on auth routes, shown on main routes

### API Client
- **Location**: `/frontend/src/lib/api.ts`
- **Purpose**: Centralized API request handling
- **Features**: JWT token attachment, error handling

## Assumptions

- Next.js 13+ with App Router is available
- Backend API endpoints are properly configured
- JWT authentication system is available
- Tailwind CSS is installed as a dependency
- The development environment supports the required technologies

## Constraints

- Only one CSS file (globals.css) is allowed
- Header must be conditionally rendered based on route
- All styling must use Tailwind utility classes
- App Router structure must be followed exactly
- No hardcoded data or mock implementations allowed

## Dependencies

- Next.js framework for routing
- Tailwind CSS for styling
- Backend API for data integration
- JWT authentication system for security
- Node.js development environment