# Research Findings: Frontend UI Technology Decisions

**Feature**: Frontend UI for Todo Web Application
**Branch**: `001-frontend-ui`
**Date**: 2026-01-08
**Status**: Complete

---

## Overview

This document consolidates research findings for all technical unknowns identified in the implementation plan. Each decision includes rationale, alternatives considered, and implementation guidance to ensure alignment with constitutional principles (especially Simplicity & Pragmatism).

---

## 1. Better Auth Integration Pattern

**Decision**: Use Better Auth React SDK with localStorage-based JWT storage and custom AuthContext wrapper.

**Rationale**:
- Better Auth provides battle-tested JWT lifecycle management (creation, storage, refresh, expiration handling)
- React SDK includes hooks (`useAuth`, `useSession`) compatible with Next.js App Router
- localStorage approach simpler than httpOnly cookies for Phase II (cookies require backend coordination for SameSite/CORS)
- Better Auth handles token refresh automatically before expiration
- Aligns with Principle VII (Simplicity) - avoid building custom auth logic

**Alternatives Considered**:
1. **NextAuth.js** - More Next.js-specific but heavier, includes OAuth providers we don't need
2. **Custom JWT management** - Violates simplicity; reinventing secure auth is high-risk
3. **httpOnly cookies** - More secure but requires backend cookie support; adds complexity for Phase II

**Implementation Notes**:
```typescript
// lib/auth/better-auth.ts
import { createAuth } from 'better-auth/client';

export const auth = createAuth({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  storage: 'localStorage', // or 'cookie' if backend supports
});

// Custom hook wrapping Better Auth
export function useAuth() {
  const { user, session, signIn, signUp, signOut, isLoading } = auth.useAuth();
  return {
    user,
    token: session?.token,
    isAuthenticated: !!session,
    isLoading,
    login: signIn,
    signup: signUp,
    logout: signOut,
  };
}
```

**XSS Mitigation**:
- Use Content Security Policy (CSP) headers to prevent inline script injection
- Sanitize all user-generated content before rendering (though task titles are plain text only)
- Better Auth SDK includes built-in XSS protection for token storage

---

## 2. API Client Architecture

**Decision**: Use native `fetch` API with custom wrapper for interceptors and error handling.

**Rationale**:
- Zero bundle size overhead (fetch is native)
- Sufficient for Phase II needs (no complex query caching, mutations, or optimistic updates beyond manual handling)
- TypeScript support via typed wrapper functions
- Interceptor pattern achievable with wrapper functions
- Aligns with Principle VII (Simplicity) - no library unless necessary

**Alternatives Considered**:
1. **Axios** - Popular but adds ~13KB gzipped; interceptors cleaner but not worth bundle cost
2. **TanStack Query (React Query)** - Excellent for caching and mutations but over-engineered for Phase II; adds complexity and bundle size
3. **SWR** - Good for data fetching but less suitable for mutations; similar complexity to TanStack Query

**Implementation Notes**:
```typescript
// lib/api/client.ts
import { auth } from '@/lib/auth/better-auth';

export class APIError extends Error {
  constructor(public code: string, public statusCode: number, message: string, public details?: any) {
    super(message);
    this.name = 'APIError';
  }
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = auth.getSession()?.token;

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers,
    }
  );

  if (!response.ok) {
    const error = await response.json();

    // Handle 401 by clearing auth and redirecting
    if (response.status === 401) {
      auth.signOut();
      window.location.href = '/login?message=session-expired';
    }

    throw new APIError(
      error.code || 'UNKNOWN_ERROR',
      response.status,
      error.error || 'An error occurred',
      error.details
    );
  }

  return response.json();
}
```

**Error Handling Pattern**:
- All API functions catch `APIError` and map to user-friendly messages
- Components use try/catch around API calls and display toasts for errors
- 401 errors handled globally (redirect to login)

---

## 3. Form Validation Strategy

**Decision**: Use React Hook Form + Zod for type-safe form validation.

**Rationale**:
- React Hook Form minimizes re-renders (uncontrolled inputs with refs)
- Zod provides runtime type validation that matches TypeScript types
- Excellent DX with `@hookform/resolvers/zod` integration
- Accessible by default (integrates with native HTML validation)
- Bundle size acceptable (~30KB combined, gzipped)

**Alternatives Considered**:
1. **Formik** - More verbose, heavier bundle (~45KB gzipped), less TypeScript-friendly
2. **Native HTML validation** - No TypeScript integration, limited validation rules, poor UX
3. **Manual validation** - Violates simplicity; error-prone and time-consuming

**Implementation Notes**:
```typescript
// lib/utils/validation.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const signupSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

export const taskSchema = z.object({
  title: z.string().min(1, 'Task title is required').max(255, 'Task title must be less than 255 characters').trim(),
});

// Usage in component
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(loginSchema),
});
```

---

## 4. State Management Approach

**Decision**: Use React Context for auth state + local useState/useReducer for task state (no global state library).

**Rationale**:
- Auth state needs sharing across components → React Context sufficient
- Task state is page-specific (dashboard only) → local state sufficient
- Optimistic updates achievable with useState + manual rollback
- Aligns with Principle VII (Simplicity) - avoid Zustand/Redux/Jotai unless complexity demands it
- Phase II scope doesn't justify global state library overhead

**Alternatives Considered**:
1. **Zustand** - Lightweight (~3KB) and simple but unnecessary for current scope
2. **Redux Toolkit** - Over-engineered for Phase II; adds significant complexity
3. **Jotai** - Atomic state management, elegant but learning curve and bundle size (~6KB) not justified

**Implementation Notes**:
```typescript
// lib/auth/AuthContext.tsx
import { createContext, useContext, ReactNode } from 'react';
import { useAuth as useBetterAuth } from './better-auth';

const AuthContext = createContext<ReturnType<typeof useBetterAuth> | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const auth = useBetterAuth();
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}

// Task state (local to dashboard page)
// app/(dashboard)/dashboard/page.tsx
function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Optimistic update example
  async function toggleTask(id: string) {
    const originalTasks = [...tasks];

    // Optimistic UI update
    setTasks(tasks.map(t => t.id === id ? { ...t, completed: !t.completed } : t));

    try {
      const updatedTask = await toggleTaskAPI(id);
      // API succeeded, update with server response
      setTasks(tasks.map(t => t.id === id ? updatedTask : t));
    } catch (error) {
      // Rollback on error
      setTasks(originalTasks);
      showToast('Failed to update task', 'error');
    }
  }
}
```

---

## 5. Optimistic UI Update Pattern

**Decision**: Manual optimistic updates with immediate setState + rollback on API error.

**Rationale**:
- Provides instant user feedback (< 100ms as required by success criteria)
- Rollback pattern simple: save original state, revert on catch
- Race condition prevention: disable button during API request
- No library needed; fits with simplicity principle

**Alternatives Considered**:
1. **TanStack Query optimistic updates** - Built-in support but requires adopting entire library
2. **Await API response before updating UI** - Violates SC-003 (100ms feedback requirement)
3. **Optimistic update without rollback** - Dangerous; leaves UI in inconsistent state on error

**Implementation Pattern**:
```typescript
// Optimistic create task
async function createTask(title: string) {
  const tempId = `temp-${Date.now()}`;
  const tempTask: Task = {
    id: tempId,
    title,
    completed: false,
    userId: user.id,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  // Optimistic add
  setTasks([...tasks, tempTask]);
  setIsCreating(true); // Disable button

  try {
    const createdTask = await createTaskAPI({ title });
    // Replace temp task with real task from server
    setTasks(tasks => tasks.map(t => t.id === tempId ? createdTask : t));
    showToast('Task created', 'success');
  } catch (error) {
    // Rollback: remove temp task
    setTasks(tasks => tasks.filter(t => t.id !== tempId));
    showToast('Failed to create task', 'error');
  } finally {
    setIsCreating(false);
  }
}

// Optimistic toggle with race prevention
async function toggleTask(id: string) {
  if (togglingIds.has(id)) return; // Prevent concurrent toggles

  setTogglingIds(new Set([...togglingIds, id])); // Disable this task's checkbox
  const originalTasks = [...tasks];

  setTasks(tasks.map(t => t.id === id ? { ...t, completed: !t.completed } : t));

  try {
    await toggleTaskAPI(id);
  } catch (error) {
    setTasks(originalTasks);
    showToast('Failed to update task', 'error');
  } finally {
    setTogglingIds(togglingIds => {
      const newSet = new Set(togglingIds);
      newSet.delete(id);
      return newSet;
    });
  }
}
```

**Race Condition Prevention**:
- Track in-flight request IDs in a Set
- Disable button/checkbox when ID is in Set
- Clear from Set in finally block

---

## 6. Responsive Design Strategy

**Decision**: Mobile-first Tailwind utility classes with responsive modifiers (sm:, md:, lg:).

**Rationale**:
- Mobile-first ensures 375px baseline always works
- Tailwind responsive modifiers are concise and readable
- No need for separate mobile/desktop components (avoids duplication)
- Touch-friendly defaults (44px tap targets) established in base styles

**Alternatives Considered**:
1. **Separate mobile/desktop components** - Duplicates code, harder to maintain
2. **Container queries** - Cutting-edge but browser support still maturing (Safari 16+), not critical for Phase II
3. **CSS media queries in separate files** - Less maintainable than inline Tailwind utilities

**Implementation Notes**:
```typescript
// Tailwind config for custom breakpoints
// tailwind.config.ts
export default {
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
    },
  },
};

// Mobile-first component example
// components/tasks/TaskCard.tsx
<div className="
  p-3                  // Mobile: 12px padding
  md:p-4               // Tablet+: 16px padding
  flex flex-col        // Mobile: stack vertically
  md:flex-row          // Tablet+: horizontal layout
  gap-2                // Mobile: 8px gap
  md:gap-4             // Tablet+: 16px gap
  min-h-[44px]         // Touch-friendly minimum height
">
  {/* Task content */}
</div>
```

**Touch-Friendly Patterns**:
- All interactive elements: `min-h-[44px] min-w-[44px]` (WCAG AA touch target)
- Buttons: `px-4 py-2` minimum (16px horizontal, 8px vertical padding)
- Checkboxes: Custom styled with `w-6 h-6` (24px, inside 44px hit area)

---

## 7. Error Handling UI Patterns

**Decision**: Use toast notifications for transient errors + inline errors for form validation + error boundaries for React crashes.

**Rationale**:
- **Toast (temporary)**: API failures, network errors, success confirmations
- **Inline (persistent)**: Form validation errors stay visible until corrected
- **Error boundary (catastrophic)**: Unhandled React errors show fallback UI instead of white screen
- Accessibility: Toasts use ARIA live regions for screen reader announcements

**Alternatives Considered**:
1. **Only inline errors** - Poor UX for transient network errors (nowhere to display)
2. **Only toasts** - Form errors disappear too quickly
3. **Modal dialogs for all errors** - Interrupts user flow, annoying for transient issues

**Implementation Notes**:
```typescript
// components/ui/Toast.tsx
import { useEffect } from 'react';

interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'info';
  onDismiss: () => void;
  duration?: number;
}

export function Toast({ message, type, onDismiss, duration = 5000 }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, duration);
    return () => clearTimeout(timer);
  }, [duration, onDismiss]);

  return (
    <div
      role="alert"
      aria-live="polite"
      className={`
        fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg
        ${type === 'error' ? 'bg-red-500 text-white' : ''}
        ${type === 'success' ? 'bg-green-500 text-white' : ''}
        ${type === 'info' ? 'bg-blue-500 text-white' : ''}
      `}
    >
      {message}
    </div>
  );
}

// lib/hooks/useToast.ts
export function useToast() {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const showToast = (message: string, type: ToastProps['type']) => {
    const id = Date.now();
    setToasts([...toasts, { id, message, type }]);
  };

  const dismissToast = (id: number) => {
    setToasts(toasts.filter(t => t.id !== id));
  };

  return { toasts, showToast, dismissToast };
}

// Error boundary
// components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

export class ErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('React Error Boundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-4">Something went wrong</h1>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Reload page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

**Error Message Mapping** (from API contracts):
- Network errors: "Network error. Please check your connection and try again."
- 401: "Your session has expired. Please log in again." (auto-redirects)
- 500: "Something went wrong. Please try again later."
- Validation errors: Display field-specific messages from API response

---

## 8. Loading State UI Patterns

**Decision**: Skeleton loaders for initial page load + spinners for button actions + disabled state for in-progress operations.

**Rationale**:
- **Skeleton loaders**: Mimic final layout, reduce perceived wait time (better UX than blank page or spinner)
- **Button spinners**: Inline feedback for create/toggle/delete actions
- **Disabled state**: Prevent duplicate submissions and race conditions
- Accessibility: Loading states announced with `aria-busy` and `aria-live`

**Alternatives Considered**:
1. **Only spinners** - Generic, doesn't convey structure of loading content
2. **Progress bars** - Misleading without real progress data (API doesn't provide upload/download progress)
3. **No loading states** - Violates FR-039, FR-040, FR-091; poor UX

**Implementation Notes**:
```typescript
// components/tasks/TaskSkeleton.tsx
export function TaskSkeleton() {
  return (
    <div className="animate-pulse flex items-center gap-3 p-4 bg-white rounded-lg border border-gray-200">
      <div className="w-6 h-6 bg-gray-300 rounded"></div>
      <div className="flex-1 space-y-2">
        <div className="h-4 bg-gray-300 rounded w-3/4"></div>
        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
      </div>
      <div className="w-8 h-8 bg-gray-300 rounded"></div>
    </div>
  );
}

// Button with loading state
// components/ui/Button.tsx
export function Button({ isLoading, children, disabled, ...props }: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      className="relative px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      {...props}
    >
      {isLoading && (
        <span className="absolute inset-0 flex items-center justify-center">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </span>
      )}
      <span className={isLoading ? 'opacity-0' : ''}>{children}</span>
    </button>
  );
}
```

**Loading State Timing**:
- Skeleton loaders: Display immediately on page load, replace with content when data arrives
- Button spinners: Show immediately on click, hide when API response received
- Minimum display time: 300ms (prevents flash of loading state for fast API responses)

---

## Summary of Decisions

| Area | Decision | Bundle Impact | Complexity |
|------|----------|---------------|------------|
| Authentication | Better Auth + localStorage | ~15KB | Low |
| API Client | Native fetch wrapper | 0KB | Low |
| Form Validation | React Hook Form + Zod | ~30KB | Low |
| State Management | React Context + useState | 0KB | Low |
| Optimistic Updates | Manual with rollback | 0KB | Medium |
| Responsive Design | Mobile-first Tailwind | 0KB (utilities) | Low |
| Error UI | Toasts + inline + boundary | ~5KB | Low |
| Loading UI | Skeletons + spinners | ~2KB | Low |
| **Total** | **~52KB added** | **Low-Medium** |

**Constitutional Alignment**:
- ✅ Principle VII (Simplicity): All decisions favor simplicity over heavy libraries
- ✅ Principle III (Auth/Security): Better Auth provides secure JWT handling
- ✅ Principle VI (Error Handling): Comprehensive error UI patterns with user-friendly messages
- ✅ All success criteria achievable with chosen stack

**Risk Assessment**:
- **Low Risk**: Form validation, responsive design, loading/error UI (standard patterns)
- **Medium Risk**: Optimistic updates (requires careful rollback logic), Better Auth integration (depends on SDK compatibility with App Router)
- **Mitigation**: Thorough testing of optimistic update edge cases; verify Better Auth examples for Next.js 15 App Router during implementation

---

## Next Actions

1. ✅ Research complete - all technical unknowns resolved
2. → Proceed to Phase 1: Create `data-model.md`, `contracts/api-client.md`, `quickstart.md`
3. → Run agent context update script
4. → Run `/sp.tasks` to generate implementation tasks
