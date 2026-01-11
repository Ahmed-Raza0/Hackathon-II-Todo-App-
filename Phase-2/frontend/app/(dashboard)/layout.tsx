import { ReactNode } from 'react';
import { Navbar } from '@/components/Navbar';
import { AuthGuard } from '@/components/auth/AuthGuard';

/**
 * Layout for dashboard pages (protected by authentication)
 * Wraps content with AuthGuard and includes Navbar
 */
export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </div>
    </AuthGuard>
  );
}
