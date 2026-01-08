/**
 * Auth configuration and utilities
 *
 * This module provides centralized authentication configuration
 * and helper functions for JWT-based auth flow.
 */

// Auth token storage key
export const AUTH_TOKEN_KEY = 'auth_token';

// Token expiration time (in milliseconds)
// Default: 7 days
export const TOKEN_EXPIRY_MS = 7 * 24 * 60 * 60 * 1000;

/**
 * Get authentication token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

/**
 * Set authentication token in localStorage
 */
export function setAuthToken(token: string): void {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.setItem(AUTH_TOKEN_KEY, token);
}

/**
 * Remove authentication token from localStorage
 */
export function clearAuthToken(): void {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

/**
 * Check if user is authenticated (has valid token)
 */
export function isAuthenticated(): boolean {
  return getAuthToken() !== null;
}

/**
 * Redirect to login page
 */
export function redirectToLogin(message?: string): void {
  if (typeof window === 'undefined') {
    return;
  }

  const url = message
    ? `/login?message=${encodeURIComponent(message)}`
    : '/login';

  window.location.href = url;
}

/**
 * Redirect to dashboard
 */
export function redirectToDashboard(): void {
  if (typeof window === 'undefined') {
    return;
  }
  window.location.href = '/dashboard';
}
