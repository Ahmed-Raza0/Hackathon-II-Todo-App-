import { apiClient } from '../lib/api';

export interface Task {
  id?: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
}

export class TaskService {
  static async getAllTasks(userId: string): Promise<Task[]> {
    return apiClient.get(`/api/${userId}/tasks`);
  }

  static async getTaskById(userId: string, taskId: number): Promise<Task> {
    return apiClient.get(`/api/${userId}/tasks/${taskId}`);
  }

  static async createTask(userId: string, task: Omit<Task, 'id'>): Promise<Task> {
    return apiClient.post(`/api/${userId}/tasks`, task);
  }

  static async updateTask(userId: string, taskId: number, task: Partial<Task>): Promise<Task> {
    return apiClient.put(`/api/${userId}/tasks/${taskId}`, task);
  }

  static async deleteTask(userId: string, taskId: number): Promise<void> {
    return apiClient.delete(`/api/${userId}/tasks/${taskId}`);
  }

  static async toggleTaskCompletion(userId: string, taskId: number, completed: boolean): Promise<Task> {
    return apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, { completed });
  }
}