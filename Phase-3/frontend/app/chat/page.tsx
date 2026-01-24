'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import ChatInterface from '@/components/chat/ChatInterface';

interface UserProfile {
  user_id: string;
  email: string;
  name: string;
}

export default function ChatPage() {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Check if token exists
        const token = apiClient.getToken();
        console.log('🔑 Token exists:', !!token);
        
        if (!token) {
          console.log('❌ No token found, redirecting to login');
          router.push('/login');
          return;
        }

        // Fetch user data
        console.log('📡 Fetching user info from /auth/me...');
        const userData = await apiClient.get<UserProfile>('/auth/me');
        console.log('✅ User data received:', userData);
        
        setUser(userData);
        setError(null);
      } catch (err: any) {
        console.error('❌ Authentication failed:', err);
        setError(err.message || 'Authentication failed');
        apiClient.clearToken();
        
        // Redirect to login after showing error
        setTimeout(() => {
          router.push('/login');
        }, 2000);
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
          <p className="mt-4 text-gray-600">Loading chat...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
            <h2 className="text-red-800 font-semibold mb-2">Authentication Error</h2>
            <p className="text-red-600 mb-4">{error}</p>
            <p className="text-sm text-gray-600">Redirecting to login...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return <ChatInterface user={user} />;
}