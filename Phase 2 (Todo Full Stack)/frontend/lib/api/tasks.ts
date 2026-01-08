import { apiClient } from './client';
import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  TaskListResponse,
  TaskResponse
} from '@/lib/types/task';

/**
 * Fetch all tasks for the authenticated user
 */
export async function getTasks(): Promise<Task[]> {
  const response = await apiClient<TaskListResponse>('/api/tasks', {
    method: 'GET',
  });

  return response.tasks;
}

/**
 * Create a new task
 */
export async function createTask(input: CreateTaskInput): Promise<Task> {
  const response = await apiClient<TaskResponse>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(input),
  });

  return response.task;
}

/**
 * Toggle task completion status
 */
export async function toggleTask(id: string): Promise<Task> {
  const response = await apiClient<TaskResponse>(`/api/tasks/${id}/toggle`, {
    method: 'PATCH',
  });

  return response.task;
}

/**
 * Update task title
 */
export async function updateTask(id: string, input: UpdateTaskInput): Promise<Task> {
  const response = await apiClient<TaskResponse>(`/api/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(input),
  });

  return response.task;
}

/**
 * Delete a task
 */
export async function deleteTask(id: string): Promise<void> {
  await apiClient<void>(`/api/tasks/${id}`, {
    method: 'DELETE',
  });
}
