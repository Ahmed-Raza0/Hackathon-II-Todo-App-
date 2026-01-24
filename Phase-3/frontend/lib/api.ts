// API Client for making authenticated requests
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ahmed-raza-phase-3-backend.hf.space/api';

class ApiClient {
  private token: string | null = null;

  constructor() {
    // Load token from localStorage on initialization (client-side only)
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        this.token = storedToken;
        console.log('🔄 Token loaded from localStorage on init');
      }
    }
  }

  setToken(token: string) {
    console.log('💾 setToken called with token:', token.substring(0, 20) + '...');
    this.token = token;
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
      localStorage.setItem('token', token);
      
      // Also set as cookie for middleware
      document.cookie = `auth_token=${token}; path=/; max-age=86400; SameSite=Lax`;
      
      console.log('✅ Token saved to localStorage and cookie');
    }
  }

  clearToken() {
    console.log('🗑️ Clearing token');
    this.token = null;
    
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('token');
      
      // Clear cookie
      document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    }
  }

  getToken(): string | null {
    // Always check localStorage for the latest token
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken && storedToken !== this.token) {
        console.log('🔄 Updating token from localStorage');
        this.token = storedToken;
      }
    }
    return this.token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
 const headers: HeadersInit & { Authorization?: string } = {
  'Content-Type': 'application/json',
  ...options.headers,
};



    // Get the latest token
    const currentToken = this.getToken();
    
    // Add authorization header if token exists
    if (currentToken) {
      headers['Authorization'] = `Bearer ${currentToken}`;
      console.log('🔑 Adding Authorization header to request');
    } else {
      console.log('⚠️ No token available for request');
    }

    const url = `${API_BASE_URL}${endpoint}`;
    
    console.log(`📡 Making ${options.method || 'GET'} request to ${endpoint}`);

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error(`❌ Request failed: ${response.status}`, errorData);
        throw new Error(
          errorData.detail || `API request failed: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      console.log(`✅ Request successful:`, data);
      return data;
    } catch (error) {
      console.error('❌ Request error:', error);
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();