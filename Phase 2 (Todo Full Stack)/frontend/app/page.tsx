import Link from 'next/link';

/**
 * Landing page - shown to unauthenticated users
 * Provides links to sign up or log in
 */
export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Hackathon Todo
        </h1>

        <p className="text-xl text-gray-700 mb-8">
          A beautiful, modern task management application.
          <br />
          Stay organized and get things done.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/signup"
            className="w-full sm:w-auto px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="w-full sm:w-auto px-8 py-3 bg-white text-primary-600 font-medium rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors border border-primary-200"
          >
            Log In
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-6 text-left">
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="text-primary-600 mb-3">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Simple & Fast</h3>
            <p className="text-sm text-gray-600">
              Quickly add, edit, and manage your tasks with an intuitive interface.
            </p>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="text-primary-600 mb-3">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Secure</h3>
            <p className="text-sm text-gray-600">
              Your tasks are private and protected with JWT authentication.
            </p>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="text-primary-600 mb-3">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Responsive</h3>
            <p className="text-sm text-gray-600">
              Works beautifully on desktop, tablet, and mobile devices.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
