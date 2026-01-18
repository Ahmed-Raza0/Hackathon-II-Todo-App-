import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, clear it and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Authentication endpoints
export const authAPI = {
  login: (credentials: { email: string; password: string }) =>
    api.post('/api/auth/login', credentials),

  register: (userData: { email: string; password: string; name?: string }) =>
    api.post('/api/auth/register', userData),

  logout: () => {
    localStorage.removeItem('access_token');
  },

  getProfile: () => api.get('/api/users/me'),
};

// Task endpoints
export const taskAPI = {
  getAll: () => api.get('/api/tasks'),

  getById: (id: string) => api.get(`/api/tasks/${id}`),

  create: (taskData: { title: string; description?: string }) =>
    api.post('/api/tasks', taskData),

  update: (id: string, taskData: { title?: string; description?: string; completed?: boolean }) =>
    api.put(`/api/tasks/${id}`, taskData),

  complete: (id: string) =>
    api.patch(`/api/tasks/${id}/complete`, { completed: true }),

  delete: (id: string) => api.delete(`/api/tasks/${id}`),
};