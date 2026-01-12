'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl overflow-hidden md:max-w-2xl border border-gray-100">
        <div className="p-10">
          <div className="text-center mb-8">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
              Todo App
            </h1>
            <p className="text-gray-600 text-lg">Manage your tasks efficiently and boost productivity</p>
          </div>

          <div className="space-y-4">
            <Link
              href="/auth/login"
              className="block w-full py-4 px-6 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white font-semibold rounded-xl transition-all duration-300 ease-in-out transform hover:-translate-y-0.5 shadow-lg hover:shadow-xl"
            >
              Sign In
            </Link>

            <Link
              href="/auth/register"
              className="block w-full py-4 px-6 bg-white border-2 border-indigo-100 hover:border-indigo-200 text-indigo-700 font-semibold rounded-xl transition-all duration-300 shadow-sm hover:shadow-md"
            >
              Create Account
            </Link>
          </div>

          <div className="mt-8 text-center text-sm text-gray-500">
            <p>Join thousands of users organizing their tasks</p>
          </div>
        </div>
      </div>
    </div>
  );
}