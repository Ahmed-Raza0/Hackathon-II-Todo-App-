'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signupSchema, type SignupFormData } from '@/lib/utils/validation';
import { signup } from '@/lib/api/auth';
import { getAuthToken } from '@/lib/auth/better-auth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { APIError } from '@/lib/types/api';

/**
 * Signup page
 * Allows new users to create an account with email and password
 * Redirects to dashboard if already authenticated
 */
export default function SignupPage() {
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
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupFormData) => {
    setIsLoading(true);
    setApiError(null);

    try {
      await signup(data);
      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (error) {
      if (error instanceof APIError) {
        if (error.code === 'EMAIL_EXISTS') {
          setApiError('An account with this email already exists. Please log in instead.');
        } else if (error.code === 'VALIDATION_ERROR') {
          setApiError('Please check your input and try again.');
        } else {
          setApiError(error.message || 'Signup failed. Please try again.');
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
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">Create Account</h2>

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
          helperText="Minimum 8 characters"
          error={errors.password?.message}
          {...register('password')}
        />

        <Input
          label="Confirm Password"
          type="password"
          placeholder="••••••••"
          error={errors.confirmPassword?.message}
          {...register('confirmPassword')}
        />

        <Button
          type="submit"
          variant="primary"
          fullWidth
          isLoading={isLoading}
        >
          {isLoading ? 'Creating account...' : 'Sign Up'}
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-gray-600">
        Already have an account?{' '}
        <Link href="/login" className="text-primary-600 hover:text-primary-700 font-medium">
          Log in
        </Link>
      </p>
    </div>
  );
}
