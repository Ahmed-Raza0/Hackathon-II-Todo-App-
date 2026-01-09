import Link from 'next/link';

/**
 * Landing page - shown to unauthenticated users
 * Provides links to sign up or log in
 */
export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-[var(--color-page-bg-start)] to-[var(--color-page-bg-end)] flex items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-5xl font-bold text-[var(--color-hero-title)] mb-4">
          Hackathon Todo
        </h1>

        <p className="text-xl text-[var(--color-hero-subtitle)] mb-8">
          A beautiful, modern task management application.
          <br />
          Stay organized and get things done.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/signup"
            className="w-full sm:w-auto px-8 py-3 bg-[var(--color-primary-cta-bg)] text-white font-semibold rounded-lg hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-cta-bg)] focus:ring-offset-2 transition-opacity"
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="w-full sm:w-auto px-8 py-3 border-2 border-[var(--color-secondary-cta-text)] text-[var(--color-secondary-cta-text)] font-medium rounded-lg hover:bg-[var(--color-secondary-cta-text)] hover:text-white focus:outline-none focus:ring-2 focus:ring-[var(--color-secondary-cta-text)] focus:ring-offset-2 transition-colors"
          >
            Log In
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-6 text-left">
          <div className="bg-[var(--color-card-bg)] p-6 rounded-xl shadow-sm border border-transparent hover:shadow-md transition-shadow">
            <div className="text-[var(--color-card-icon)] mb-3">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-[var(--color-card-heading)] mb-2">Simple & Fast</h3>
            <p className="text-sm text-[var(--color-card-body)]">
              Quickly add, edit, and manage your tasks with an intuitive interface.
            </p>
          </div>

          <div className="bg-[var(--color-card-bg)] p-6 rounded-xl shadow-sm border border-transparent hover:shadow-md transition-shadow">
            <div className="text-[var(--color-card-icon)] mb-3">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="font-semibold text-[var(--color-card-heading)] mb-2">Secure</h3>
            <p className="text-sm text-[var(--color-card-body)]">
              Your tasks are private and protected with JWT authentication.
            </p>
          </div>

          <div className="bg-[var(--color-card-bg)] p-6 rounded-xl shadow-sm border border-transparent hover:shadow-md transition-shadow">
            <div className="text-[var(--color-card-icon)] mb-3">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-[var(--color-card-heading)] mb-2">Responsive</h3>
            <p className="text-sm text-[var(--color-card-body)]">
              Works beautifully on desktop, tablet, and mobile devices.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
