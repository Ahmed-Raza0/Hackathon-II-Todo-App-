'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { logout } from '@/lib/api/auth';
import { Button } from '@/components/ui/Button';

interface LogoutButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  className?: string;
}

/**
 * LogoutButton component
 * Handles user logout with loading state
 */
export function LogoutButton({ variant = 'ghost', className }: LogoutButtonProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleLogout = async () => {
    setIsLoading(true);

    try {
      await logout();
      // Redirect to landing page
      router.push('/');
    } catch (error) {
      // Even if API call fails, we've cleared local storage
      // So still redirect to landing page
      router.push('/');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      onClick={handleLogout}
      variant={variant}
      isLoading={isLoading}
      className={className}
    >
      {isLoading ? 'Logging out...' : 'Log Out'}
    </Button>
  );
}
