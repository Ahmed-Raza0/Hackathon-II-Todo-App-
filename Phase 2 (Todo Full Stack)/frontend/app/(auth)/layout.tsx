import { ReactNode } from 'react';

/**
 * Layout for authentication pages (login, signup)
 * Provides centered layout with branding
 */
export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Hackathon Todo</h1>
          <p className="text-gray-600 mt-2">Manage your tasks with ease</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          {children}
        </div>
      </div>
    </div>
  );
}
