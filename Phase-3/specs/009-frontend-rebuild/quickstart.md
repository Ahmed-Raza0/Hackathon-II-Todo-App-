# Quickstart Guide: Frontend Rebuild Implementation

## Overview
This guide explains how to work with the rebuilt frontend that follows the SP-FRONTEND-REBUILD specification. The frontend has been completely rebuilt with proper Tailwind CSS integration and backend connectivity.

## Project Structure
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
 │   │   └── Header.tsx
 │   └── lib
 │       └── api.ts
 ├── tailwind.config.ts
 ├── postcss.config.js
 ├── next.config.js
 └── package.json
```

## Getting Started

### 1. Environment Setup
1. Ensure you're in the `/frontend` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

### 2. Key Configuration Files
- **API Client**: `/frontend/src/lib/api.ts` - Centralized API requests with JWT
- **Global Styles**: `/frontend/src/app/globals.css` - Tailwind directives only
- **Layout**: `/frontend/src/app/layout.tsx` - Root layout with conditional header
- **Tailwind Config**: `tailwind.config.ts` - Content paths for class detection

### 3. Adding New Pages
1. Create new directories in `/src/app/`
2. Add a `page.tsx` file in the new directory
3. The header will automatically show/hide based on the route rules:
   - Show on: '/', '/tasks', '/chat'
   - Hide on: '/login', '/signup'

### 4. Making API Calls
Use the centralized API client:
```ts
import { taskAPI } from '@/lib/api';

// Create a task
await taskAPI.create({ title: 'New task', description: 'Description' });

// Get all tasks
const tasks = await taskAPI.getAll();
```

### 5. Styling Components
- Only use Tailwind utility classes
- No inline styles allowed
- Use semantic color classes (e.g., `text-primary`, `bg-secondary`)
- Follow consistent spacing patterns (e.g., `p-4`, `m-2`, `space-y-4`)

## Validation Checklist
- [x] Tailwind CSS classes are applied correctly
- [x] Header shows/hides based on route rules
- [x] All API calls include JWT tokens
- [x] No inline styles exist in components
- [x] Pages have meaningful content (no blank pages)
- [x] Navigation works between all routes
- [x] Backend integration functions properly

## Troubleshooting

### CSS Not Loading
- Verify `globals.css` has the correct Tailwind directives
- Check that `layout.tsx` imports `globals.css`
- Confirm `tailwind.config.ts` has correct content paths

### API Requests Failing
- Verify JWT token is properly attached to requests
- Check that the backend API is running
- Confirm API endpoints match the backend specification

### Header Showing on Auth Pages
- Review the route matching logic in the Header component
- Ensure login/signup routes are properly handled

## Best Practices
- Use the centralized API client for all backend requests
- Follow the header visibility rules strictly
- Apply Tailwind classes consistently
- Test route-based header visibility
- Validate JWT token inclusion in all authenticated requests