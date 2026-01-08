'use client';

import { useState } from 'react';
import type { Task } from '@/lib/types/task';
import { cn } from '@/lib/utils/cn';

interface TaskCardProps {
  task: Task;
  onToggle: (id: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onEdit: (id: string, title: string) => Promise<void>;
}

/**
 * TaskCard component - displays a single task
 *
 * Features:
 * - Checkbox to toggle completion status
 * - Strikethrough and muted styling for completed tasks
 * - Delete button with confirmation dialog
 * - Loading states for toggle and delete operations
 * - Timestamp display
 *
 * @example
 * ```tsx
 * <TaskCard
 *   task={task}
 *   onToggle={handleToggle}
 *   onDelete={handleDelete}
 * />
 * ```
 */
export function TaskCard({ task, onToggle, onDelete, onEdit }: TaskCardProps) {
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleToggle = async () => {
    if (isToggling) return;

    setIsToggling(true);
    try {
      await onToggle(task.id);
    } catch (error) {
      // Error handling done by parent (toast notification)
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (isDeleting) return;

    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } catch (error) {
      // Error handling done by parent (toast notification)
      setShowDeleteConfirm(false);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleEdit = async () => {
    if (isEditing) return;

    setIsEditing(true);
    setEditTitle(task.title);
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) return;

    setIsEditing(false);
    try {
      await onEdit(task.id, editTitle.trim());
    } catch (error) {
      // Error handling done by parent (toast notification)
      setIsEditing(true); // Stay in edit mode on error
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditTitle(task.title); // Reset to original title
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
  };

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-center gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={cn(
            'flex-shrink-0 h-5 w-5 rounded border-2 transition-all focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
            task.completed
              ? 'bg-primary-600 border-primary-600'
              : 'border-gray-300 hover:border-primary-500',
            isToggling && 'opacity-50 cursor-not-allowed'
          )}
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed && (
            <svg
              className="h-full w-full text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        {/* Task content or edit form */}
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="flex flex-col gap-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 text-base border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSaveEdit();
                  } else if (e.key === 'Escape') {
                    handleCancelEdit();
                  }
                }}
                autoFocus
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSaveEdit}
                  disabled={!editTitle.trim()}
                  className="px-3 py-1.5 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Save
                </button>
                <button
                  onClick={handleCancelEdit}
                  className="px-3 py-1.5 bg-gray-200 text-gray-900 text-sm rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-1"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex-1 min-w-0">
                <p
                  className={cn(
                    'text-base font-medium break-words',
                    task.completed
                      ? 'line-through text-gray-400'
                      : 'text-gray-900'
                  )}
                >
                  {task.title}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {formatDate(task.createdAt)}
                </p>
              </div>

              <div className="flex gap-2">
                {/* Edit button */}
                <button
                  onClick={handleEdit}
                  className="flex-shrink-0 p-2 text-gray-400 hover:text-primary-600 rounded-lg hover:bg-primary-50 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                  aria-label="Edit task"
                >
                  <svg
                    className="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                </button>

                {/* Delete button */}
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  disabled={isDeleting}
                  className="flex-shrink-0 p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Delete task"
                >
                  <svg
                    className="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Delete confirmation dialog */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-sm w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Delete Task?
            </h3>
            <p className="text-sm text-gray-600 mb-6">
              Are you sure you want to delete "{task.title}"? This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                disabled={isDeleting}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
