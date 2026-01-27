'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-lg">
        <div className="text-center">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-4">
            Todo App
          </h1>

          <p className="text-lg text-gray-600 mb-8">
            Manage your tasks efficiently with our intuitive platform.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/signup"
              className="w-full sm:w-auto px-6 py-3 rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:text-lg"
            >
              Sign Up
            </a>

            <a
              href="/login"
              className="w-full sm:w-auto px-6 py-3 rounded-md border border-gray-300 text-gray-700 hover:bg-gray-50 md:text-lg"
            >
              Log In
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
