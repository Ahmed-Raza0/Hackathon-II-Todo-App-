// Session management for Better Auth

import { authClient } from './auth';

// Session management functions
export class SessionManager {
  // Get current session
  static async getSession() {
    try {
      // Using Better Auth client to get session
      const session = await authClient.getSession();
      return session;
    } catch (error) {
      console.error('Error getting session:', error);
      return null;
    }
  }

  // Sign in user
  static async signIn(credentials: { email: string; password: string }) {
    try {
      const response = await authClient.signIn.email({
        email: credentials.email,
        password: credentials.password,
        callbackURL: '/dashboard',
      });
      return response;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  }

  // Sign up user
  static async signUp(userData: { email: string; password: string; name?: string }) {
    try {
      const response = await authClient.signUp.email({
        email: userData.email,
        password: userData.password,
        name: userData.name || '',
        callbackURL: '/dashboard',
      });
      return response;
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  }

  // Sign out user
  static async signOut() {
    try {
      await authClient.signOut({
        callbackURL: '/',
      });
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  }

  // Check if user is authenticated
  static async isAuthenticated(): Promise<boolean> {
    try {
      const session = await this.getSession();
      return !!session;
    } catch (error) {
      console.error('Auth check error:', error);
      return false;
    }
  }
}