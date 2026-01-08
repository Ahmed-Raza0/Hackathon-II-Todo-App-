import type { Task } from '@/lib/types/task';
import { TaskCard } from '@/components/tasks/TaskCard';

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onEdit: (id: string, title: string) => Promise<void>;
  isLoading?: boolean;
}

/**
 * TaskList component - displays a list of tasks
 *
 * Features:
 * - Empty state message when no tasks
 * - Task cards for each task
 * - Loading state support
 *
 * @example
 * ```tsx
 * <TaskList
 *   tasks={tasks}
 *   onToggle={handleToggle}
 *   onDelete={handleDelete}
 *   onEdit={handleEdit}
 * />
 * ```
 */
export function TaskList({ tasks, onToggle, onDelete, onEdit, isLoading }: TaskListProps) {
  if (isLoading) {
    return null; // Loading handled by parent
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto h-24 w-24 text-gray-200 mb-6">
          <svg
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2M12 15l-3-3m0 0l3-3m-3 3h6"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
        <p className="text-gray-500">
          Get started by creating your first task above.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
}