'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, type LoginFormData } from '@/lib/utils/validation';
import { login } from '@/lib/api/auth';
import { getAuthToken } from '@/lib/auth/better-auth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { APIError } from '@/lib/types/api';

/**
 * Login page
 * Allows existing users to log in with email and password
 * Redirects to dashboard if already authenticated
 */
export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // Redirect if already authenticated
  useEffect(() => {
    const token = getAuthToken();
    if (token) {
      router.push('/dashboard');
    }
  }, [router]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setApiError(null);

    try {
      await login(data);
      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (error) {
      if (error instanceof APIError) {
        if (error.code === 'INVALID_CREDENTIALS') {
          setApiError('Invalid email or password. Please try again.');
        } else {
          setApiError(error.message || 'Login failed. Please try again.');
        }
      } else {
        setApiError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">Log In</h2>

      {apiError && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {apiError}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="Email"
          type="email"
          placeholder="you@example.com"
          error={errors.email?.message}
          {...register('email')}
        />

        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          error={errors.password?.message}
          {...register('password')}
        />

        <Button
          type="submit"
          variant="primary"
          fullWidth
          isLoading={isLoading}
        >
          {isLoading ? 'Logging in...' : 'Log In'}
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-gray-600">
        Don't have an account?{' '}
        <Link href="/signup" className="text-primary-600 hover:text-primary-700 font-medium">
          Sign up
        </Link>
      </p>
    </div>
  );
}
