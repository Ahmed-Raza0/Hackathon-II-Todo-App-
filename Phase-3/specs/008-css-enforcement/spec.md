# SP-CSS-ENFORCEMENT – Mandatory Tailwind CSS Loading & UI Quality Specification

This **SP-SPECIFY** exists because pages are rendering **WITHOUT CSS**, resulting in broken UI and poor user experience. This spec is **non-negotiable** and must be enforced before any UI/UX judgment or feature work.

## SP-CSS-01: Problem Statement

Observed failures:

• Pages render as plain HTML (no styling)
• Tailwind utility classes have no effect
• UI looks unprofessional regardless of component design

**Root cause is ALWAYS configuration or import violation, never Tailwind itself.**

## SP-CSS-02: Non-Negotiable Rules

1. **CSS Must Load Before UI Review** – Any UI without CSS is INVALID.
2. **Single Global CSS Entry** – Only one global CSS file allowed.
3. **No Page-Level CSS Imports** – Pages must NEVER import CSS.
4. **Tailwind Only** – Custom CSS, inline styles, or external frameworks are FORBIDDEN.

## SP-CSS-03: Canonical Global CSS Location

### REQUIRED FILE

```
/frontend/src/app/globals.css
```

### REQUIRED CONTENT (Exact)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

❌ Any additional CSS is forbidden at this stage.

## SP-CSS-04: Mandatory CSS Import Point

### File

```
/frontend/src/app/layout.tsx
```

### REQUIRED IMPORT (Top of file)

```ts
import './globals.css'
```

❌ Importing CSS anywhere else is forbidden.

## SP-CSS-05: Tailwind Configuration Contract

### File

```
/frontend/tailwind.config.ts
```

### REQUIRED CONFIG

```ts
content: [
  './src/**/*.{ts,tsx}',
]
```

If this path is wrong → **CSS will NEVER load**.

## SP-CSS-06: PostCSS Contract

### File

```
/frontend/postcss.config.js
```

### REQUIRED CONTENT

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

Missing file = NO CSS.

## SP-CSS-07: Forbidden Failure Patterns

❌ `globals.css` in `/styles`
❌ Importing CSS in `page.tsx`
❌ Wrong `content` path in Tailwind config
❌ Multiple CSS files
❌ Expecting Tailwind without restart

## SP-CSS-08: Mandatory Restart Rule

After ANY change to:

• `tailwind.config.ts`
• `postcss.config.js`
• `globals.css`

You MUST:

```
CTRL+C
npm run dev
```

Hot reload is NOT sufficient.

## SP-CSS-09: Validation Procedure

1. Open browser DevTools
2. Inspect any element
3. Confirm Tailwind classes appear in computed styles

If not → spec violation.

## SP-CSS-10: UI Quality Gate

UI/UX evaluation is **FORBIDDEN** until:

✔ Tailwind styles visibly apply
✔ Layout spacing works
✔ Colors render correctly

## SP-CSS-11: Supremacy Clause

Hierarchy:

**Constitution > SP-SRC > SP-CSS-ENFORCEMENT > All UI Specs > Code**

If CSS is missing, all UI specs are PAUSED.

---

## User Scenarios & Testing

### Scenario 1: CSS Loading Verification
**Given**: A developer opens the application in a browser
**When**: The page renders
**Then**: Elements display with proper Tailwind styling
**Validation**: Check that Tailwind classes are applied in computed styles via DevTools

### Scenario 2: New Component Styling
**Given**: A developer creates a new component with Tailwind classes
**When**: The component is rendered
**Then**: Tailwind styles are applied correctly
**Validation**: Visual inspection and DevTools verification

### Scenario 3: Configuration Change
**Given**: A developer modifies tailwind.config.ts
**When**: The development server is restarted
**Then**: All Tailwind classes continue to work properly
**Validation**: All pages maintain proper styling after restart

## Functional Requirements

### FR-01: Global CSS File Management
**Requirement**: The system must have a single, canonical global CSS file.
**Acceptance Criteria**:
- File exists at `/frontend/src/app/globals.css`
- File contains only the required Tailwind directives
- No additional CSS is added to this file

### FR-02: CSS Import Verification
**Requirement**: The global CSS file must be imported at the application root.
**Acceptance Criteria**:
- `globals.css` is imported in `/frontend/src/app/layout.tsx`
- No other pages or components import CSS directly
- CSS is applied globally to all pages

### FR-03: Tailwind Configuration Compliance
**Requirement**: The Tailwind configuration must include the correct content paths.
**Acceptance Criteria**:
- `tailwind.config.ts` includes `./src/**/*.{ts,tsx}` in content paths
- All Tailwind classes are properly detected and generated
- No classes are missing from the final CSS

### FR-04: PostCSS Configuration
**Requirement**: The PostCSS configuration must properly reference Tailwind.
**Acceptance Criteria**:
- `postcss.config.js` exists and properly configures Tailwind plugin
- CSS processing pipeline works correctly
- Tailwind directives are processed correctly

## Success Criteria

### Quantitative Measures
- 100% of Tailwind utility classes render correctly on all pages
- 0% of inline styles or custom CSS exists in components
- 100% of pages load with proper styling
- 0% of CSS import violations exist in pages/components

### Qualitative Measures
- UI appears professionally styled with consistent spacing and typography
- All interactive elements have proper hover/focus states
- Responsive design works correctly across screen sizes
- Color scheme is consistent and professional

## Key Entities

### Global CSS File
- **Location**: `/frontend/src/app/globals.css`
- **Purpose**: Single entry point for all global styles
- **Content**: Only Tailwind directives (@tailwind base/components/utilities)

### Tailwind Configuration
- **Location**: `/frontend/tailwind.config.ts`
- **Purpose**: Configure Tailwind to scan correct files
- **Content**: Proper content paths for class detection

### Layout Component
- **Location**: `/frontend/src/app/layout.tsx`
- **Purpose**: Root component that imports global CSS
- **Function**: Ensures CSS is available to all child components

## Assumptions

- The project uses Next.js App Router structure
- Tailwind CSS is already installed as a dependency
- The development environment supports hot reloading after configuration changes
- All developers follow the single global CSS file approach

## Constraints

- Only one global CSS file is allowed
- No inline styles or custom CSS in components
- Tailwind is the only accepted CSS framework
- All configuration files must be in their canonical locations

## Dependencies

- Next.js framework for the app router structure
- Tailwind CSS library for utility classes
- PostCSS for CSS processing
- Node.js development environment