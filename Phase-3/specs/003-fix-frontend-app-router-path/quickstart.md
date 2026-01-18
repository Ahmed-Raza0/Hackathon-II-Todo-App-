# Quickstart Guide: Frontend App Router Path Resolution

**Feature**: 003-fix-frontend-app-router-path
**Date**: 2026-01-16
**Status**: Draft

## Purpose

This guide provides instructions to implement the canonical Next.js App Router structure as specified in SP-SRC, ensuring proper routing and eliminating conflicts between multiple app directory structures.

## Prerequisites

- Node.js LTS installed
- Next.js project with potential conflicting app directories
- Access to modify project structure

## Implementation Steps

### 1. Verify Current Structure
First, check if conflicting app directories exist:
```bash
ls -la frontend/app/  # Check if this exists (FORBIDDEN)
ls -la frontend/src/app/  # Check if this exists (CANONICAL)
```

### 2. Apply Canonical Structure
If `/frontend/app` exists, remove it and ensure canonical structure exists:
```bash
rm -rf frontend/app/  # Remove forbidden structure
mkdir -p frontend/src/app/
```

### 3. Create Required Files
Ensure required files exist in canonical location:

**Create frontend/src/app/layout.tsx**:
```tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo App Phase III',
  description: 'Todo application for Phase III',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

**Create frontend/src/app/page.tsx**:
```tsx
export default function Home() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Todo App Phase III</h1>
    </main>
  )
}
```

**Create frontend/src/app/globals.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
```

### 4. Validate Implementation
After restructuring, verify the implementation:
```bash
npm run dev
```

Then navigate to http://localhost:3000/ to confirm the home page renders without 404 errors.

## Validation Checklist

- [ ] Only `/frontend/src/app/` exists (not `/frontend/app/`)
- [ ] `frontend/src/app/page.tsx` exists and exports default component
- [ ] `frontend/src/app/layout.tsx` exists and wraps `{children}`
- [ ] `frontend/src/app/globals.css` exists
- [ ] Development server starts without router conflicts
- [ ] Home page renders at http://localhost:3000/
- [ ] No 404 errors occur

## Troubleshooting

**Problem**: Development server fails to start after changes
**Solution**: Ensure all required files exist in the canonical location and check for import path errors

**Problem**: 404 error when accessing home page
**Solution**: Verify that `page.tsx` exists in the canonical location with proper default export

**Problem**: Multiple app directories detected
**Solution**: Remove any non-canonical app directories (`/frontend/app/`) as specified in SP-SRC-05