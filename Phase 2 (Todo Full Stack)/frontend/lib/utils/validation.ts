import { z } from 'zod';

// Auth validation schemas
export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const signupSchema = z
  .object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword'], // Attach error to confirmPassword field
  });

// Task validation schemas
export const createTaskSchema = z.object({
  title: z
    .string()
    .min(1, 'Task title is required')
    .max(255, 'Task title must be less than 255 characters')
    .trim(),
});

export const updateTaskSchema = z.object({
  title: z
    .string()
    .min(1, 'Task title is required')
    .max(255, 'Task title must be less than 255 characters')
    .trim(),
});

// Type inference from schemas
export type LoginFormData = z.infer<typeof loginSchema>;
export type SignupFormData = z.infer<typeof signupSchema>;
export type CreateTaskFormData = z.infer<typeof createTaskSchema>;
export type UpdateTaskFormData = z.infer<typeof updateTaskSchema>;
