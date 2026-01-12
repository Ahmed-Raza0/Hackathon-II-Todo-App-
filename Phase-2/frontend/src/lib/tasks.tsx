'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from './auth';
import toast from 'react-hot-toast';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
  user_id: string;
}

interface TaskCreateData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

interface TaskUpdateData {
  title?: string;
  description?: string;
  status?: 'pending' | 'in-progress' | 'completed';
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

interface TasksContextType {
  tasks: Task[];
  addTask: (data: TaskCreateData) => Promise<void>;
  updateTask: (id: string, data: TaskUpdateData) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

const TasksContext = createContext<TasksContextType | undefined>(undefined);

export function TasksProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    if (!user) return;

    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const tasksData = await response.json();
        setTasks(tasksData);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to fetch tasks');
      }
    } catch (err) {
      setError('Network error occurred while fetching tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const addTask = async (data: TaskCreateData) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const newTask = await response.json();
      setTasks(prev => [newTask, ...prev]);
      toast.success('Task added successfully!');
      return newTask;
    } else {
      const errorData = await response.json();
      const errorMessage = errorData.detail || 'Failed to add task';
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const updateTask = async (id: string, data: TaskUpdateData) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const updatedTask = await response.json();
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      toast.success('Task updated successfully!');
      return updatedTask;
    } else {
      const errorData = await response.json();
      const errorMessage = errorData.detail || 'Failed to update task';
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const deleteTask = async (id: string) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      setTasks(prev => prev.filter(task => task.id !== id));
      toast.success('Task deleted successfully!');
    } else {
      const errorData = await response.json();
      const errorMessage = errorData.detail || 'Failed to delete task';
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const value = {
    tasks,
    addTask,
    updateTask,
    deleteTask,
    isLoading,
    error,
  };

  return <TasksContext.Provider value={value}>{children}</TasksContext.Provider>;
};

export function useTasks() {
  const context = useContext(TasksContext);
  if (context === undefined) {
    throw new Error('useTasks must be used within a TasksProvider');
  }
  return context;
}