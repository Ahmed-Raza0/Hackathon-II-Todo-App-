import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { createTaskSchema, updateTaskSchema, type CreateTaskFormData, type UpdateTaskFormData } from '@/lib/utils/validation';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

interface TaskFormProps {
  initialTitle?: string;
  onSave: (title: string) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  mode?: 'create' | 'edit';
}

/**
 * TaskForm component - handles both task creation and editing
 *
 * Features:
 * - Form validation with Zod schema
 * - Loading states
 * - Save/cancel actions
 * - Different modes for create vs edit
 *
 * @example
 * ```tsx
 * <TaskForm
 *   initialTitle="Existing task title"
 *   onSave={handleSave}
 *   onCancel={handleCancel}
 *   mode="edit"
 * />
 * ```
 */
export function TaskForm({
  initialTitle = '',
  onSave,
  onCancel,
  isLoading = false,
  mode = 'create'
}: TaskFormProps) {
  const schema = mode === 'edit' ? updateTaskSchema : createTaskSchema;

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreateTaskFormData | UpdateTaskFormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      title: initialTitle,
    },
  });

  const onSubmit = async (data: CreateTaskFormData | UpdateTaskFormData) => {
    try {
      await onSave(data.title);
      reset(); // Reset form after successful save
    } catch (error) {
      // Error handling done by parent component
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex gap-3">
      <div className="flex-1">
        <Input
          {...register('title')}
          placeholder={mode === 'edit' ? 'Edit task title...' : 'What needs to be done?'}
          error={errors.title?.message}
          disabled={isLoading}
          autoFocus={true}
        />
      </div>
      <div className="flex gap-2">
        <Button
          type="submit"
          variant="primary"
          isLoading={isLoading}
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : (mode === 'edit' ? 'Save' : 'Add')}
        </Button>
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
}
