'use client';

import { useState, useEffect, useCallback } from 'react';
import type { Task, CreateTaskInput, UpdateTaskInput } from '@/lib/types/task';
import * as taskAPI from '@/lib/api/tasks';
import { APIError } from '@/lib/types/api';

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  createTask: (input: CreateTaskInput) => Promise<void>;
  toggleTask: (id: string) => Promise<void>;
  updateTask: (id: string, input: UpdateTaskInput) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  refreshTasks: () => Promise<void>;
}

/**
 * Custom hook for managing task state with optimistic updates
 *
 * Features:
 * - Automatic task fetching on mount
 * - Optimistic updates for create, toggle, update, delete
 * - Automatic rollback on API failure
 * - Loading and error states
 *
 * @example
 * ```tsx
 * function TaskDashboard() {
 *   const { tasks, isLoading, createTask, toggleTask, deleteTask } = useTasks();
 *
 *   if (isLoading) return <TaskSkeleton />;
 *
 *   return (
 *     <TaskList
 *       tasks={tasks}
 *       onToggle={toggleTask}
 *       onDelete={deleteTask}
 *     />
 *   );
 * }
 * ```
 */
export function useTasks(): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks on mount
  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const fetchedTasks = await taskAPI.getTasks();
      setTasks(fetchedTasks);
    } catch (err) {
      const errorMessage = err instanceof APIError ? err.message : 'Failed to load tasks';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Create task with optimistic update
  const createTask = useCallback(async (input: CreateTaskInput) => {
    // Optimistic update: add temporary task
    const tempId = `temp-${Date.now()}`;
    const optimisticTask: Task = {
      id: tempId,
      title: input.title,
      completed: false,
      userId: 'current-user', // Will be replaced by API response
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    setTasks((prev) => [optimisticTask, ...prev]);

    try {
      const newTask = await taskAPI.createTask(input);
      // Replace temporary task with real task from API
      setTasks((prev) => prev.map((t) => (t.id === tempId ? newTask : t)));
    } catch (err) {
      // Rollback: remove temporary task
      setTasks((prev) => prev.filter((t) => t.id !== tempId));
      throw err;
    }
  }, []);

  // Toggle task completion with optimistic update
  const toggleTask = useCallback(async (id: string) => {
    // Store previous state for rollback
    const previousTasks = tasks;

    // Optimistic update: toggle completed status
    setTasks((prev) =>
      prev.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );

    try {
      const updatedTask = await taskAPI.toggleTask(id);
      // Update with real task from API
      setTasks((prev) => prev.map((t) => (t.id === id ? updatedTask : t)));
    } catch (err) {
      // Rollback: restore previous state
      setTasks(previousTasks);
      throw err;
    }
  }, [tasks]);

  // Update task with optimistic update
  const updateTask = useCallback(async (id: string, input: UpdateTaskInput) => {
    // Store previous state for rollback
    const previousTasks = tasks;

    // Optimistic update: update title
    setTasks((prev) =>
      prev.map((task) =>
        task.id === id ? { ...task, title: input.title, updatedAt: new Date().toISOString() } : task
      )
    );

    try {
      const updatedTask = await taskAPI.updateTask(id, input);
      // Update with real task from API
      setTasks((prev) => prev.map((t) => (t.id === id ? updatedTask : t)));
    } catch (err) {
      // Rollback: restore previous state
      setTasks(previousTasks);
      throw err;
    }
  }, [tasks]);

  // Delete task with optimistic update
  const deleteTask = useCallback(async (id: string) => {
    // Store previous state for rollback
    const previousTasks = tasks;

    // Optimistic update: remove task
    setTasks((prev) => prev.filter((task) => task.id !== id));

    try {
      await taskAPI.deleteTask(id);
    } catch (err) {
      // Rollback: restore previous state
      setTasks(previousTasks);
      throw err;
    }
  }, [tasks]);

  return {
    tasks,
    isLoading,
    error,
    createTask,
    toggleTask,
    updateTask,
    deleteTask,
    refreshTasks: fetchTasks,
  };
}
