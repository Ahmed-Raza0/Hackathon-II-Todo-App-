'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import TaskManager from '@/components/tasks/TaskManager';

interface UserProfile {
  user_id: string;
  email: string;
  name: string;
}

export default function TasksPage() {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const token = apiClient.getToken();
      
      if (!token) {
        router.push('/login');
        return;
      }

      try {
        // Fetch current user from your backend
        const userData = await apiClient.get<UserProfile>('/auth/me');
        setUser(userData);
      } catch (error) {
        console.error('Authentication failed:', error);
        apiClient.clearToken();
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <TaskManager user={user} />
    </div>
  );
}