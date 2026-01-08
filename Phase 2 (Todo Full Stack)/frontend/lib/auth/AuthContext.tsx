'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { AuthState, User, LoginCredentials, SignupCredentials } from '@/lib/types/auth';
import * as authAPI from '@/lib/api/auth';
import { getAuthToken, clearAuthToken } from '@/lib/auth/better-auth';

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  signup: (credentials: SignupCredentials) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = () => {
      const token = getAuthToken();

      if (token) {
        // Token exists - user is authenticated
        // In a real app, you might want to validate the token with the backend
        // For now, we'll just mark as authenticated
        setAuthState({
          user: null, // User data will be fetched when needed
          token,
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        // No token - user is not authenticated
        setAuthState({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    };

    initializeAuth();
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    try {
      const response = await authAPI.login(credentials);

      setAuthState({
        user: response.user,
        token: response.token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      // Clear any stale auth state
      clearAuthToken();
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
      throw error; // Re-throw so calling component can handle
    }
  }, []);

  const signup = useCallback(async (credentials: SignupCredentials) => {
    try {
      const response = await authAPI.signup(credentials);

      setAuthState({
        user: response.user,
        token: response.token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      // Clear any stale auth state
      clearAuthToken();
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
      throw error; // Re-throw so calling component can handle
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authAPI.logout();
    } finally {
      // Always clear local state, even if API call fails
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  }, []);

  const value: AuthContextType = {
    ...authState,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access auth context
 * Use this in components to access auth state and actions
 */
export function useAuthContext(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }

  return context;
}
