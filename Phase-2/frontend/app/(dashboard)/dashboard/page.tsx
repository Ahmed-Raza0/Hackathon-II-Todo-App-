'use client';

import { useState } from 'react';
import { useTasks } from '@/lib/hooks/useTasks';
import { useToast } from '@/lib/hooks/useToast';
import { TaskList } from '@/components/tasks/TaskList';
import { TaskSkeleton } from '@/components/tasks/TaskSkeleton';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ToastContainer } from '@/components/ui/Toast';

/**
 * Dashboard page - main view for authenticated users
 * Allows viewing, creating, toggling, and deleting tasks
 */
export default function DashboardPage() {
  const { tasks, isLoading, error, createTask, toggleTask, deleteTask, updateTask } = useTasks();
  const { showSuccess, showError, toasts, dismiss } = useToast();
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      showError('Task title cannot be empty');
      return;
    }

    if (newTaskTitle.length > 255) {
      showError('Task title must be less than 255 characters');
      return;
    }

    setIsCreating(true);

    try {
      await createTask({ title: newTaskTitle.trim() });
      setNewTaskTitle('');
      showSuccess('Task created successfully!');
    } catch (err) {
      showError('Failed to create task. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <p className="text-gray-600">{tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}</p>
      </div>

      {/* Create task form */}
      <form onSubmit={handleCreateTask} className="mb-6">
        <div className="flex gap-3">
          <div className="flex-1">
            <Input
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              placeholder="What needs to be done?"
              error=""
              disabled={isCreating}
            />
          </div>
          <Button
            type="submit"
            variant="primary"
            isLoading={isCreating}
            disabled={!newTaskTitle.trim()}
          >
            {isCreating ? 'Adding...' : 'Add'}
          </Button>
        </div>
      </form>

      {/* Error display */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {error}
        </div>
      )}

      {/* Loading state */}
      {isLoading && <TaskSkeleton />}

      {/* Task list */}
      {!isLoading && (
        <TaskList
          tasks={tasks}
          onToggle={async (id: string) => {
            try {
              await toggleTask(id);
              showSuccess('Task updated successfully!');
            } catch (err) {
              showError('Failed to update task. Please try again.');
            }
          }}
          onEdit={async (id: string, title: string) => {
            try {
              await updateTask(id, { title });
              showSuccess('Task updated successfully!');
            } catch (err) {
              showError('Failed to update task. Please try again.');
            }
          }}
          onDelete={async (id: string) => {
            try {
              await deleteTask(id);
              showSuccess('Task deleted successfully!');
            } catch (err) {
              showError('Failed to delete task. Please try again.');
            }
          }}
          isLoading={isLoading}
        />
      )}

      <ToastContainer toasts={toasts} onDismiss={dismiss} />
    </div>
  );
}