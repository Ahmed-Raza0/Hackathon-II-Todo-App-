import { APIError } from '@/lib/types/api';

/**
 * Base API client using native fetch with automatic token attachment
 * and error handling.
 */
export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get token from localStorage (will be managed by Better Auth)
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Attach Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${process.env.NEXT_PUBLIC_API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle non-OK responses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        error: 'An error occurred',
        code: 'UNKNOWN_ERROR',
      }));

      // Handle 401 Unauthorized - clear auth and redirect
      if (response.status === 401) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          window.location.href = '/login?message=session-expired';
        }
      }

      throw new APIError(
        errorData.code || 'UNKNOWN_ERROR',
        response.status,
        errorData.error || 'An error occurred',
        errorData.details
      );
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    // Parse JSON response
    return response.json();
  } catch (error) {
    // Handle network errors
    if (error instanceof APIError) {
      throw error;
    }

    throw new APIError(
      'NETWORK_ERROR',
      0,
      'Network error. Please check your connection and try again.'
    );
  }
}
