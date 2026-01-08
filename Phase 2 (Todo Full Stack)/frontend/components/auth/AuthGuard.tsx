'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { getAuthToken } from '@/lib/auth/better-auth';

interface AuthGuardProps {
  children: ReactNode;
}

/**
 * AuthGuard component - protects routes that require authentication
 *
 * Redirects to /login if user is not authenticated
 *
 * @example
 * ```tsx
 * <AuthGuard>
 *   <DashboardContent />
 * </AuthGuard>
 * ```
 */
export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter();

  useEffect(() => {
    const token = getAuthToken();

    if (!token) {
      // No token found - redirect to login
      router.push('/login?message=authentication-required');
    }
  }, [router]);

  // Check token immediately (for SSR)
  const token = getAuthToken();

  if (!token) {
    // Show loading or blank screen while redirecting
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
