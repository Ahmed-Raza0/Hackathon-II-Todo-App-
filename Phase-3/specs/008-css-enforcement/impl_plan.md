# SP-CSS-ENFORCEMENT – Implementation Plan (Mandatory Tailwind CSS Loading & UI Quality)

This **Implementation Plan** defines the step-by-step approach for implementing the **SP-CSS-ENFORCEMENT** specification to ensure proper Tailwind CSS loading and UI quality.

## Technical Context

The current issue is that pages are rendering without CSS, resulting in broken UI and poor user experience. This is caused by configuration or import violations rather than Tailwind itself. The implementation will enforce a single global CSS file with proper Tailwind directives and ensure all components follow the correct import pattern.

## Constitution Check

The implementation aligns with the project constitution by:
- Following the non-negotiable rules of CSS loading before UI review
- Maintaining a single global CSS entry point
- Enforcing Tailwind-only styling approach
- Preserving the hierarchical structure of specifications

## Gates

### Gate 1: Pre-implementation Validation
- [x] SP-CSS-ENFORCEMENT specification is approved
- [x] Current CSS state assessed
- [x] Development server can be stopped/restarted

### Gate 2: Implementation Prerequisites
- [x] Node.js and npm available
- [x] Tailwind CSS installed as dependency
- [x] Next.js App Router structure confirmed

## Phase 0: Research & Analysis

### R0.1: Current State Assessment
**Task**: Research current CSS implementation status in the application
**Decision**: Need to verify which CSS files exist, their content, and how they're being imported
**Rationale**: Understanding current state is critical to implement the required changes correctly
**Alternatives considered**: Manual inspection vs automated analysis - chose manual inspection for accuracy

### R0.2: Tailwind Configuration Review
**Task**: Research current tailwind.config.ts and postcss.config.js settings
**Decision**: Need to understand current content paths and plugin configurations
**Rationale**: Required to ensure proper Tailwind class detection and generation
**Alternatives considered**: Assuming defaults vs checking actual configuration - chose to check actual

## Phase 1: Implementation & Design

### Task 1: Create/Verify Global CSS File
**Location**: `/frontend/src/app/globals.css`
**Action**: Ensure file exists with correct content:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Task 2: Verify CSS Import in Layout
**Location**: `/frontend/src/app/layout.tsx`
**Action**: Ensure file imports global CSS:
```ts
import './globals.css'
```

### Task 3: Update Tailwind Configuration
**Location**: `/frontend/tailwind.config.ts`
**Action**: Ensure content path is correct:
```ts
content: [
  './src/**/*.{ts,tsx}',
]
```

### Task 4: Create PostCSS Configuration
**Location**: `/frontend/postcss.config.js`
**Action**: Ensure file exists with correct content:
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Task 5: Remove Forbidden CSS Practices
**Action**:
- Remove any CSS imports in page components
- Remove inline styles where possible
- Consolidate multiple CSS files into the global file

### Task 6: Restart Development Server
**Action**: Stop and restart the dev server to apply all configuration changes

## Data Model

This implementation does not involve data modeling as it's purely a CSS/styling concern.

## API Contracts

This implementation does not involve API changes as it's focused on CSS configuration.

## Quickstart Guide

### For Developers
1. Verify the global CSS file exists at `/frontend/src/app/globals.css`
2. Confirm the layout imports the CSS: `import './globals.css'`
3. Ensure tailwind.config.ts has the correct content paths
4. Verify postcss.config.js is properly configured
5. Restart the dev server after any configuration changes

### Testing
1. Open browser DevTools
2. Inspect any element
3. Confirm Tailwind classes appear in computed styles

## Agent Context Update

The implementation reinforces the following patterns:
- Single global CSS entry point
- Tailwind-only styling approach
- Proper configuration file placement
- Required server restart after config changes