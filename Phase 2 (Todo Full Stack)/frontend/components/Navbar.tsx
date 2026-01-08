'use client';

import Link from 'next/link';
import { LogoutButton } from '@/components/auth/LogoutButton';

/**
 * Navbar component
 * Displayed on authenticated pages with app name and logout button
 */
export function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link
            href="/dashboard"
            className="text-xl font-bold text-gray-900 hover:text-primary-600 transition-colors"
          >
            Hackathon Todo
          </Link>

          <div className="flex items-center gap-4">
            <LogoutButton variant="ghost" />
          </div>
        </div>
      </div>
    </nav>
  );
}
