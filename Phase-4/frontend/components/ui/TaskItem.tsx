'use client';

import { Task } from '@/services/taskService';
import { useState } from 'react';

interface TaskItemProps {
  task: Task;
  onToggle: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (task: Task) => void;
}

export default function TaskItem({ task, onToggle, onDelete, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleSave = () => {
    onUpdate({
      ...task,
      title: editTitle,
      description: editDescription,
    });
    setIsEditing(false);
  };

  return (
    <div className="border rounded-lg p-4 mb-2 bg-white shadow-sm">
      {isEditing ? (
        <div>
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full border rounded p-2 mb-2"
            placeholder="Task title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full border rounded p-2 mb-2"
            placeholder="Task description"
          />
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
            >
              Save
            </button>
            <button
              onClick={() => setIsEditing(false)}
              className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggle(task)}
              className="mr-2 mt-1"
            />
            <div className="flex-1">
              <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : ''}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                  {task.description}
                </p>
              )}
              <p className="text-xs text-gray-400 mt-1">
                Created: {new Date(task.created_at || '').toLocaleString()}
                {task.updated_at && `, Updated: ${new Date(task.updated_at).toLocaleString()}`}
              </p>
            </div>
            <div className="flex space-x-1">
              <button
                onClick={() => setIsEditing(true)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id!)}
                className="text-red-500 hover:text-red-700 ml-2"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}