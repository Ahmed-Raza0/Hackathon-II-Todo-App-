# Quickstart Guide: SP-CSS-ENFORCEMENT Implementation

## Overview
This guide explains how to implement and maintain the SP-CSS-ENFORCEMENT specification for proper Tailwind CSS loading and UI quality.

## Core Requirements

### 1. Global CSS File
- **Location**: `/frontend/src/app/globals.css`
- **Content**: Must contain only:
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```
- **Rule**: No additional CSS allowed in this file

### 2. CSS Import Pattern
- **Location**: `/frontend/src/app/layout.tsx`
- **Import**: Must import globals.css at the top of the file
- **Rule**: CSS imported only in root layout, nowhere else

### 3. Tailwind Configuration
- **Location**: `/frontend/tailwind.config.ts`
- **Content**: Must include correct content paths:
  ```ts
  content: [
    './src/**/*.{ts,tsx}',
  ]
  ```
- **Rule**: All source files must be included in content paths

### 4. PostCSS Configuration
- **Location**: `/frontend/postcss.config.js`
- **Content**: Must configure Tailwind and Autoprefixer:
  ```js
  module.exports = {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  }
  ```
- **Rule**: Required for proper CSS processing

## Implementation Steps

### Step 1: Verify Global CSS
1. Check that `/frontend/src/app/globals.css` exists
2. Verify it contains only the three required Tailwind directives
3. Remove any additional CSS if present

### Step 2: Verify Import Pattern
1. Check that `/frontend/src/app/layout.tsx` imports globals.css
2. Ensure no other pages/components import CSS directly
3. Remove any page-level CSS imports if found

### Step 3: Update Configuration Files
1. Update `tailwind.config.ts` with correct content paths
2. Create/update `postcss.config.js` with proper plugin configuration
3. Verify all paths are correct

### Step 4: Restart Development Server
1. Stop the current dev server (Ctrl+C)
2. Restart with `npm run dev`
3. **Important**: Configuration changes require a full restart

## Testing and Validation

### CSS Loading Verification
1. Open browser DevTools
2. Inspect any element on the page
3. Confirm Tailwind classes appear in computed styles
4. Verify elements render with proper styling

### UI Quality Check
1. Navigate to all application pages
2. Verify consistent spacing, typography, and colors
3. Confirm responsive design works correctly
4. Ensure interactive elements have proper hover/focus states

## Common Issues and Solutions

### Issue: CSS Not Loading
**Symptoms**: Pages render as plain HTML with no styling
**Solution**:
1. Verify globals.css has correct Tailwind directives
2. Check that layout.tsx imports globals.css
3. Restart dev server after configuration changes

### Issue: Tailwind Classes Not Working
**Symptoms**: Tailwind classes in components don't apply styles
**Solution**:
1. Verify tailwind.config.ts has correct content paths
2. Ensure dev server was restarted after config changes
3. Check for typos in class names

### Issue: Mixed Styling Approaches
**Symptoms**: Some components use inline styles or custom CSS
**Solution**:
1. Replace inline styles with Tailwind classes
2. Remove custom CSS files beyond globals.css
3. Refactor components to use Tailwind utility classes

## Maintenance Guidelines

### Adding New Styles
- Use Tailwind utility classes only
- No custom CSS in components
- Add new classes to globals.css only if absolutely necessary

### Configuration Changes
- Always restart dev server after changing config files
- Test thoroughly after configuration updates
- Update content paths when adding new source directories

### Component Development
- Use Tailwind classes for all styling
- Follow consistent design patterns
- Test responsiveness across screen sizes