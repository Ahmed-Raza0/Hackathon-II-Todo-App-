# Data Model: SP-FRONTEND-REBUILD Implementation

## Overview
This implementation focuses on frontend structure and integration rather than creating new data models. However, it interacts with existing backend data models through API contracts and enforces proper frontend architecture.

## Frontend Configuration Entities

### Global CSS Configuration
- **Location**: `/frontend/src/app/globals.css`
- **Purpose**: Single entry point for all global styles using Tailwind directives
- **Content**: @tailwind base, @tailwind components, @tailwind utilities
- **Constraints**: No additional CSS allowed beyond Tailwind directives

### Layout Component
- **Location**: `/frontend/src/app/layout.tsx`
- **Purpose**: Root layout that wraps all pages and manages global CSS import
- **Responsibilities**: Import globals.css, conditionally render Header, wrap all pages
- **Constraints**: Must be the only place for global CSS import

### Header Component
- **Location**: `/frontend/src/components/Header.tsx`
- **Purpose**: Navigation component with conditional visibility based on route
- **Responsibilities**: Provide navigation links, hide on auth routes, show on main routes
- **Constraints**: Must follow route-based visibility rules

### API Client
- **Location**: `/frontend/src/lib/api.ts`
- **Purpose**: Centralized API request handling with JWT authentication
- **Responsibilities**: Attach JWT token to requests, handle errors, normalize responses
- **Constraints**: Must be the single source for all API requests

## Page Components

### Dashboard Page
- **Location**: `/frontend/src/app/page.tsx`
- **Purpose**: Main dashboard showing welcome content
- **Content**: Welcome heading and short description
- **Constraints**: Must show Header component

### Tasks Page
- **Location**: `/frontend/src/app/tasks/page.tsx`
- **Purpose**: Task management interface with add form and list
- **Content**: Empty state, add task form, task list
- **Constraints**: Must show Header component

### Chat Page
- **Location**: `/frontend/src/app/chat/page.tsx`
- **Purpose**: Chat interface with input and message display
- **Content**: Intro message, chat input placeholder
- **Constraints**: Must show Header component

### Login Page
- **Location**: `/frontend/src/app/login/page.tsx`
- **Purpose**: User authentication interface
- **Content**: Login form UI
- **Constraints**: Must NOT show Header component

### Signup Page
- **Location**: `/frontend/src/app/signup/page.tsx`
- **Purpose**: User registration interface
- **Content**: Signup form UI
- **Constraints**: Must NOT show Header component

## Integration Entities

### Tailwind Configuration
- **Location**: `/frontend/tailwind.config.ts`
- **Purpose**: Configure Tailwind to scan correct files and generate appropriate CSS
- **Content**: Content paths and theme extensions
- **Constraints**: Must include './src/**/*.{ts,tsx}' in content paths

### PostCSS Configuration
- **Location**: `/frontend/postcss.config.js`
- **Purpose**: Configure PostCSS plugins for Tailwind and Autoprefixer
- **Content**: Plugin configuration for tailwindcss and autoprefixer
- **Constraints**: Must properly reference Tailwind plugin

### Next.js Configuration
- **Location**: `/frontend/next.config.js`
- **Purpose**: Configure Next.js build and runtime behavior
- **Content**: Framework-specific configuration options
- **Constraints**: Must align with App Router requirements

## Validation Rules

### CSS Enforcement Rules
- Only globals.css may contain CSS directives
- No CSS imports allowed in page components
- All styling must use Tailwind utility classes
- No inline styles permitted in components

### Header Visibility Rules
- Show Header on: '/', '/tasks', '/chat'
- Hide Header on: '/login', '/signup'
- Header must be conditionally rendered based on current route

### API Integration Rules
- All requests must go through the centralized API client
- JWT tokens must be attached to authenticated requests
- Error responses must be handled appropriately
- No direct fetch calls outside the API client

### Component Architecture Rules
- Pages must not import CSS directly
- Components must rely on global CSS
- Navigation must use next/link for proper routing
- Form submissions must use the API client for backend communication