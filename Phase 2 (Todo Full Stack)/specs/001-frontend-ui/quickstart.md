# Quickstart Guide: Frontend UI Development

**Feature**: Frontend UI for Todo Web Application
**Branch**: `001-frontend-ui`
**Date**: 2026-01-08

---

## Overview

This guide helps developers set up the local development environment, understand the project structure, and perform common development tasks for the Todo Frontend UI. Follow these steps to get the application running and begin implementation.

---

## Prerequisites

Ensure the following tools are installed:

- **Node.js**: 18.x or later (LTS recommended)
- **npm**: 9.x or later (comes with Node.js)
- **Git**: For version control
- **Code Editor**: VS Code recommended (with TypeScript, ESLint, Tailwind CSS IntelliSense extensions)

**Optional but Recommended**:
- **pnpm** or **yarn** as alternative package managers
- **Postman** or **Insomnia** for testing backend API endpoints manually

---

## Initial Setup

### 1. Clone Repository (if not already cloned)

```bash
cd "D:/Hackathon II (Todo App)/Phase 2 (Todo Full Stack)"
```

The repository should already be cloned and you should be on the `001-frontend-ui` branch.

### 2. Navigate to Frontend Directory

**Note**: During initial implementation, you may need to create the `frontend/` directory first.

```bash
# If frontend/ directory doesn't exist yet
mkdir frontend
cd frontend
```

### 3. Initialize Next.js Project

**If starting from scratch** (run once during task execution):

```bash
# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"

# Answer prompts:
# ✔ Would you like to use ESLint? … Yes
# ✔ Would you like to use Tailwind CSS? … Yes
# ✔ Would you like to use `src/` directory? … No
# ✔ Would you like to use App Router? … Yes
# ✔ Would you like to customize the default import alias? … No (use @/*)
```

**If project already initialized** (subsequent setups):

```bash
# Install dependencies
npm install
```

### 4. Install Additional Dependencies

```bash
# Authentication
npm install better-auth

# Form handling and validation
npm install react-hook-form @hookform/resolvers zod

# Utilities
npm install clsx tailwind-merge

# Icons (choose one)
npm install lucide-react  # or: npm install @heroicons/react

# Date formatting (if needed)
npm install date-fns

# Development dependencies
npm install -D @types/node @types/react @types/react-dom
```

### 5. Environment Configuration

Create `.env.local` file in `frontend/` directory:

```bash
# Create environment file
touch .env.local
```

Add the following content to `.env.local`:

```bash
# Backend API Base URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# App Configuration (optional)
NEXT_PUBLIC_APP_NAME="Hackathon Todo"
```

**Important**: Never commit `.env.local` to version control (already in `.gitignore` by default).

### 6. Create Project Structure

Create the directory structure as defined in `plan.md`:

```bash
# From frontend/ directory
mkdir -p app/{(auth)/login,(auth)/signup,(dashboard)/dashboard}
mkdir -p components/{auth,tasks,ui}
mkdir -p lib/{api,auth,hooks,utils,types}
mkdir -p public/images
mkdir -p tests/{e2e,components}
```

---

## Development Workflow

### Running the Development Server

```bash
# Start Next.js development server
npm run dev

# Server runs on http://localhost:3000
# Open in browser: http://localhost:3000
```

**Features**:
- Hot Module Replacement (HMR) - changes reflect immediately
- Fast Refresh - preserves component state during edits
- TypeScript error checking in terminal
- Automatic port assignment if 3000 is occupied

### Building for Production

```bash
# Create optimized production build
npm run build

# Output: .next/ directory with compiled application
# Build includes:
# - Static page generation
# - Bundle optimization and minification
# - TypeScript type checking
# - ESLint validation
```

### Starting Production Server

```bash
# After building
npm start

# Runs production build on http://localhost:3000
```

### Running Tests

```bash
# Run all unit tests (once tests are written)
npm test

# Run tests in watch mode (re-runs on file changes)
npm test -- --watch

# Run tests with coverage report
npm test -- --coverage

# Run E2E tests (requires app to be running)
npm run test:e2e
```

**Test Commands** (add to `package.json` if not present):
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test"
  }
}
```

---

## Code Quality Tools

### Linting

```bash
# Run ESLint to check for code issues
npm run lint

# Fix auto-fixable linting issues
npm run lint -- --fix
```

### Formatting (if Prettier is configured)

```bash
# Format all files
npm run format

# Check formatting without modifying files
npm run format:check
```

**Add to `package.json`** (if not present):
```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

### Type Checking

```bash
# Run TypeScript compiler in check mode (no emit)
npm run type-check
```

**Add to `package.json`**:
```json
{
  "scripts": {
    "type-check": "tsc --noEmit"
  }
}
```

---

## Project Structure Overview

```
frontend/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Route group for unauthenticated pages
│   │   ├── login/page.tsx        # Login page: /login
│   │   ├── signup/page.tsx       # Signup page: /signup
│   │   └── layout.tsx            # Auth layout (centered card)
│   ├── (dashboard)/              # Route group for authenticated pages
│   │   ├── dashboard/page.tsx    # Dashboard: /dashboard
│   │   └── layout.tsx            # Dashboard layout (navbar + auth guard)
│   ├── layout.tsx                # Root layout (HTML, fonts, global styles)
│   ├── page.tsx                  # Landing page: /
│   └── globals.css               # Tailwind + custom CSS variables
├── components/                   # Reusable React components
│   ├── auth/                     # Authentication-related components
│   │   ├── AuthForm.tsx          # Shared auth form (login/signup)
│   │   ├── AuthGuard.tsx         # Route protection HOC
│   │   └── LogoutButton.tsx      # Logout button with confirmation
│   ├── tasks/                    # Task management components
│   │   ├── TaskCard.tsx          # Individual task item
│   │   ├── TaskForm.tsx          # Create/edit task form
│   │   ├── TaskList.tsx          # Task list container
│   │   └── TaskSkeleton.tsx      # Loading skeleton
│   ├── ui/                       # Generic UI primitives
│   │   ├── Button.tsx            # Button component
│   │   ├── Input.tsx             # Input component
│   │   ├── Toast.tsx             # Toast notification
│   │   └── Modal.tsx             # Modal/dialog
│   ├── Navbar.tsx                # Main navigation bar
│   └── ErrorBoundary.tsx         # React error boundary
├── lib/                          # Business logic and utilities
│   ├── api/                      # API client functions
│   │   ├── client.ts             # Base API client (fetch wrapper)
│   │   ├── auth.ts               # Auth API functions
│   │   └── tasks.ts              # Task API functions
│   ├── auth/                     # Authentication logic
│   │   └── better-auth.ts        # Better Auth configuration
│   ├── hooks/                    # Custom React hooks
│   │   ├── useAuth.ts            # Auth state and operations
│   │   ├── useTasks.ts           # Task state and CRUD operations
│   │   └── useToast.ts           # Toast notification state
│   ├── utils/                    # Utility functions
│   │   ├── cn.ts                 # Class name merger (Tailwind)
│   │   └── validation.ts         # Zod validation schemas
│   └── types/                    # TypeScript type definitions
│       ├── auth.ts               # Auth-related types
│       ├── task.ts               # Task-related types
│       └── api.ts                # API response types
├── public/                       # Static assets
│   ├── images/                   # Images and illustrations
│   │   └── empty-state.svg       # Empty state illustration
│   └── favicon.ico               # Site favicon
├── tests/                        # Test files
│   ├── e2e/                      # End-to-end tests
│   │   ├── auth.spec.ts          # Auth flow tests
│   │   └── tasks.spec.ts         # Task CRUD tests
│   └── components/               # Component unit tests
│       ├── TaskCard.test.tsx     # TaskCard tests
│       └── TaskForm.test.tsx     # TaskForm tests
├── .env.local                    # Environment variables (not committed)
├── .eslintrc.json                # ESLint configuration
├── .gitignore                    # Git ignore rules
├── next.config.js                # Next.js configuration
├── package.json                  # Dependencies and scripts
├── tailwind.config.ts            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── README.md                     # Project documentation
```

---

## Common Development Tasks

### 1. Adding a New Page

Next.js App Router uses file-system routing. Create a `page.tsx` file in the desired route directory.

**Example**: Add a 404 page

```bash
# Create not-found page
touch app/not-found.tsx
```

```tsx
// app/not-found.tsx
export default function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">404</h1>
        <p className="text-gray-600 mb-4">Page not found</p>
        <a href="/" className="text-blue-500 hover:underline">Go home</a>
      </div>
    </div>
  );
}
```

### 2. Creating a New Component

Create component files in `components/<category>/ComponentName.tsx`.

**Example**: Create a Button component

```bash
touch components/ui/Button.tsx
```

```tsx
// components/ui/Button.tsx
import { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '@/lib/utils/cn';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
  children: ReactNode;
}

export function Button({
  variant = 'primary',
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  const variantClasses = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-500 text-white hover:bg-red-600',
  };

  return (
    <button
      disabled={disabled || isLoading}
      className={cn(
        'px-4 py-2 rounded-lg font-medium transition-colors',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  );
}
```

### 3. Adding API Functions

Add API functions to `lib/api/<domain>.ts`.

**Example**: Add createTask function

```typescript
// lib/api/tasks.ts
import { apiClient } from './client';
import type { Task, CreateTaskInput, TaskResponse } from '@/lib/types/task';

export async function createTask(input: CreateTaskInput): Promise<Task> {
  const response = await apiClient<TaskResponse>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(input),
  });
  return response.task;
}
```

### 4. Creating Custom Hooks

Add hooks to `lib/hooks/useHookName.ts`.

**Example**: useTasks hook

```typescript
// lib/hooks/useTasks.ts
import { useState, useEffect } from 'react';
import { getTasks, createTask, toggleTask, deleteTask } from '@/lib/api/tasks';
import type { Task, CreateTaskInput } from '@/lib/types/task';

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  async function loadTasks() {
    try {
      setIsLoading(true);
      const fetchedTasks = await getTasks();
      setTasks(fetchedTasks);
    } catch (err) {
      setError('Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  }

  async function addTask(input: CreateTaskInput) {
    const newTask = await createTask(input);
    setTasks([...tasks, newTask]);
  }

  async function toggleTaskStatus(id: string) {
    const updatedTask = await toggleTask(id);
    setTasks(tasks.map(t => t.id === id ? updatedTask : t));
  }

  async function removeTask(id: string) {
    await deleteTask(id);
    setTasks(tasks.filter(t => t.id !== id));
  }

  return {
    tasks,
    isLoading,
    error,
    addTask,
    toggleTaskStatus,
    removeTask,
    refreshTasks: loadTasks,
  };
}
```

### 5. Updating Tailwind Configuration

Customize design tokens in `tailwind.config.ts`.

**Example**: Add custom colors and spacing

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [],
};

export default config;
```

### 6. Defining TypeScript Types

Add types to `lib/types/<domain>.ts`.

**Example**: Task types

```typescript
// lib/types/task.ts
export interface Task {
  id: string;
  title: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTaskInput {
  title: string;
}

export interface UpdateTaskInput {
  title: string;
}

export interface TaskListResponse {
  tasks: Task[];
}

export interface TaskResponse {
  task: Task;
}
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_APP_NAME` | Application name | `"Hackathon Todo"` |

**Note**: `NEXT_PUBLIC_` prefix makes variables accessible in browser code. Variables without this prefix are server-side only.

---

## Troubleshooting

### Issue: Port 3000 already in use

**Solution**:
```bash
# Kill process on port 3000 (Windows)
npx kill-port 3000

# Or specify a different port
npm run dev -- -p 3001
```

### Issue: Module not found errors

**Solution**:
```bash
# Clear Next.js cache and reinstall dependencies
rm -rf .next node_modules package-lock.json
npm install
```

### Issue: TypeScript errors not showing in VS Code

**Solution**:
1. Restart TypeScript server: Cmd/Ctrl + Shift + P → "TypeScript: Restart TS Server"
2. Check `tsconfig.json` is correctly configured
3. Ensure VS Code is using workspace TypeScript version

### Issue: Tailwind classes not applying

**Solution**:
1. Check `tailwind.config.ts` content paths include your files
2. Restart dev server (`npm run dev`)
3. Clear browser cache
4. Ensure `globals.css` imports Tailwind directives:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

### Issue: API requests failing with CORS errors

**Solution**:
- Ensure backend is running and has CORS configured to allow `http://localhost:3000`
- Check `NEXT_PUBLIC_API_BASE_URL` in `.env.local` is correct
- Verify backend API endpoints match contract in `contracts/api-client.md`

---

## Helpful Commands Reference

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Run production server |
| `npm run lint` | Lint code with ESLint |
| `npm run lint -- --fix` | Fix linting issues automatically |
| `npm test` | Run unit tests |
| `npm test -- --watch` | Run tests in watch mode |
| `npm run type-check` | Check TypeScript types |
| `npx kill-port 3000` | Kill process on port 3000 |
| `rm -rf .next` | Clear Next.js build cache |

---

## Next Steps

1. ✅ Development environment set up
2. → Run `/sp.tasks` to generate implementation tasks
3. → Begin implementation starting with project setup tasks (P1)
4. → Follow task priorities (P1 → P2 → P3) for systematic development
5. → Test each feature as implemented (unit tests + manual testing)

---

## Additional Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **React Documentation**: https://react.dev
- **Tailwind CSS Documentation**: https://tailwindcss.com/docs
- **TypeScript Handbook**: https://www.typescriptlang.org/docs
- **Better Auth Docs**: https://better-auth.com/docs
- **React Hook Form**: https://react-hook-form.com
- **Zod Documentation**: https://zod.dev

For project-specific questions, refer to:
- `spec.md` - Feature requirements and user stories
- `plan.md` - Implementation plan and technical context
- `data-model.md` - TypeScript interfaces and validation rules
- `contracts/api-client.md` - API endpoint specifications
