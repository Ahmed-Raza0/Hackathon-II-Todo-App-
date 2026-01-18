# SP-EMPTY-PAGES-UI-AUTH – Empty Pages, Professional Colors, Tailwind Enforcement & Auth Header Rules

This **SP-SPECIFY** authoritatively defines:

• What content MUST appear when pages are empty
• A professional, locked color system
• Mandatory Tailwind CSS enforcement ("Tailwind never works" issue)
• Conditional Header visibility (hidden on Sign In / Sign Up)

This spec is **binding** and overrides ad‑hoc UI fixes.

## SP-EPUA-01: Purpose

Resolve the following frontend failures:

• Pages render empty or confusing
• No professional color harmony
• Tailwind classes appear to "not work"
• Header incorrectly visible on auth routes

## SP-EPUA-02: Non‑Negotiable Rules

1. **No Blank Pages** – Every route MUST render meaningful empty-state content
2. **Single Color System** – No random Tailwind colors
3. **Tailwind or Nothing** – Inline CSS & custom CSS files are FORBIDDEN
4. **Auth Isolation** – Header MUST NOT render on `/login` or `/signup`

## SP-EPUA-03: Approved Color Combination (Professional)

### Semantic Palette (Locked)

| Purpose    | Tailwind Classes                  |
| ---------- | --------------------------------- |
| Background | `bg-background text-foreground`   |
| Primary    | `text-indigo-600` `bg-indigo-600` |
| Secondary  | `text-slate-600`                  |
| Border     | `border-border`                   |
| Success    | `text-green-600`                  |
| Error      | `text-red-600`                    |

❌ Hex colors, `style={{}}`, or random colors are FORBIDDEN.

## SP-EPUA-04: Tailwind Enforcement Specification

### Required Checks

1. `globals.css` MUST include:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

2. `tailwind.config.ts` MUST include:

```ts
content: ['./src/**/*.{ts,tsx}']
```

3. All UI styling MUST be Tailwind utility classes

If Tailwind appears broken → **spec violation, not bug**.

## SP-EPUA-05: Header Visibility Rules (Critical)

### Header MUST render on:

• `/`
• `/tasks`
• `/chat`

### Header MUST NOT render on:

• `/login`
• `/signup`

### Enforcement Location

```
/frontend/src/app/layout.tsx
```

Header rendering MUST be conditional based on route.

## SP-EPUA-06: Empty Page Content Specification

### Empty Tasks Page

User sees:

• Icon
• Message: "No tasks yet"
• CTA button: "Add your first task"

No blank screens allowed.

### Empty Chat Page

User sees:

• Message: "Start a conversation"
• Subtext explaining AI usage

### Empty Dashboard

User sees:

• Welcome message
• Short app explanation

## SP-EPUA-07: Functional Requirements (All Pages)

Each page MUST:

• Handle loading state
• Handle empty state
• Handle error state
• Reflect backend truth only

## SP-EPUA-08: Forbidden Patterns

❌ Header duplicated inside pages
❌ Fake counters or static data
❌ Pages with only headings
❌ Tailwind + custom CSS mix

## SP-EPUA-09: Validation Checklist

✔ Tailwind utilities visibly applied
✔ Colors consistent across pages
✔ Header hidden on auth routes
✔ Empty pages informative
✔ No inline styles

## SP-EPUA-10: Supremacy Clause

Hierarchy:

**Constitution > SP-SRC > SP-FRONTEND-NEG > SP-UIUX-PRO > SP-UIUX-PRO-BE > SP-EPUA**

If UI fails → check this spec BEFORE writing code.

---

## User Scenarios & Testing

### Scenario 1: User Visits Login Page
**Given**: User navigates to `/login`
**When**: Page loads
**Then**: Header is not visible
**Validation**: No navigation header appears on authentication pages

### Scenario 2: User Visits Tasks Page with No Tasks
**Given**: User is authenticated and has no tasks
**When**: Tasks page loads
**Then**: User sees empty state with icon, message "No tasks yet", and CTA button "Add your first task"
**Validation**: Meaningful content appears instead of blank page

### Scenario 3: User Visits Main Dashboard
**Given**: User navigates to `/`
**When**: Page loads
**Then**: Header is visible
**Validation**: Navigation header appears on main application routes

### Scenario 4: User Sees Consistent Styling
**Given**: User navigates through the application
**When**: Different pages load
**Then**: Consistent professional color scheme is applied
**Validation**: All pages use approved Tailwind color classes only

## Functional Requirements

### FR-01: Empty State Management
**Requirement**: Every page must render meaningful content when empty.
**Acceptance Criteria**:
- Empty pages display appropriate messaging based on page context
- Empty states include clear calls to action where appropriate
- No blank or confusing empty screens are presented to users

### FR-02: Color System Enforcement
**Requirement**: All UI elements must use the approved color palette.
**Acceptance Criteria**:
- Only approved Tailwind color classes are used in the UI
- No inline styles or custom CSS colors are present
- Color consistency is maintained across all pages

### FR-03: Tailwind CSS Compliance
**Requirement**: All styling must be implemented using Tailwind CSS classes.
**Acceptance Criteria**:
- globals.css contains the required Tailwind directives
- tailwind.config.ts includes proper content paths
- No custom CSS files or inline styles are used for presentation

### FR-04: Conditional Header Rendering
**Requirement**: Header must be conditionally rendered based on route.
**Acceptance Criteria**:
- Header appears on main application routes (/, /tasks, /chat)
- Header is hidden on authentication routes (/login, /signup)
- No duplicate header implementations exist in individual pages

## Success Criteria

### Quantitative Measures
- 100% of pages display meaningful content when empty (0% blank screens)
- 100% of UI elements use approved Tailwind color classes (0% custom colors)
- 100% of styling implemented with Tailwind classes (0% inline/custom CSS)
- 100% of auth routes hide the header component

### Qualitative Measures
- Users experience consistent professional color scheme throughout the application
- Users never see blank or confusing empty states
- Users can navigate efficiently with appropriate header visibility
- Application presents polished, cohesive visual design

## Key Entities

### Header Component
- **Purpose**: Navigation element for main application routes
- **Visibility Rules**: Conditionally rendered based on route
- **Placement**: Should be implemented in layout component

### Empty State Components
- **Purpose**: Informative content displayed when data is absent
- **Variants**: Different messages for different page contexts (tasks, chat, etc.)
- **Elements**: Icons, descriptive text, call-to-action buttons

## Assumptions

- The application uses Next.js App Router with layout.tsx for shared components
- Tailwind CSS is already configured in the project
- Authentication routes are clearly defined as /login and /signup
- The color palette defined in the specification is sufficient for all UI needs

## Constraints

- All styling must use Tailwind CSS utility classes only
- Header component must be conditionally rendered based on route
- Only approved color palette may be used
- Empty states must be meaningful and provide value to users

## Dependencies

- Next.js App Router for layout and conditional rendering
- Tailwind CSS framework for styling
- React for component implementation
- Routing system to determine current page for header visibility