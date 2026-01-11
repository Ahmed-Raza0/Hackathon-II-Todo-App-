import { useAuthContext } from '@/lib/auth/AuthContext';

/**
 * Custom hook for accessing authentication state and actions
 *
 * This is a convenience wrapper around useAuthContext that provides
 * a cleaner API for components to consume auth functionality.
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, login, logout } = useAuth();
 *
 *   if (!isAuthenticated) {
 *     return <LoginForm onSubmit={login} />;
 *   }
 *
 *   return (
 *     <div>
 *       <p>Welcome, {user?.email}</p>
 *       <button onClick={logout}>Logout</button>
 *     </div>
 *   );
 * }
 * ```
 */
export function useAuth() {
  return useAuthContext();
}
