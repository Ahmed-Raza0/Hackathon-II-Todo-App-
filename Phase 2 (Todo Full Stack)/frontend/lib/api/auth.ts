import { apiClient } from './client';
import type { AuthResponse, LoginCredentials, SignupCredentials } from '@/lib/types/auth';

/**
 * Sign up a new user
 */
export async function signup(credentials: SignupCredentials): Promise<AuthResponse> {
  const response = await apiClient<AuthResponse>('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify({
      email: credentials.email,
      password: credentials.password,
    }),
  });

  // Store token in localStorage
  if (typeof window !== 'undefined' && response.token) {
    localStorage.setItem('auth_token', response.token);
  }

  return response;
}

/**
 * Log in an existing user
 */
export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  const response = await apiClient<AuthResponse>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });

  // Store token in localStorage
  if (typeof window !== 'undefined' && response.token) {
    localStorage.setItem('auth_token', response.token);
  }

  return response;
}

/**
 * Log out the current user
 */
export async function logout(): Promise<void> {
  try {
    // Attempt to call backend logout endpoint (optional)
    await apiClient('/api/auth/logout', {
      method: 'POST',
    });
  } catch (error) {
    // Ignore errors - we'll clear token anyway
  } finally {
    // Always clear token from localStorage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }
}
