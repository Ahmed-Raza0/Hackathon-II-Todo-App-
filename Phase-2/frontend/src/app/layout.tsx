import { AuthProvider } from '../lib/auth';
import { TasksProvider } from '../lib/tasks';
import { Toaster } from 'react-hot-toast';
import '../styles/globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        <AuthProvider>
          <TasksProvider>
            <div className="min-h-screen bg-gray-50">
              {children}
            </div>
            <Toaster position="top-right" toastOptions={{
              style: {
                background: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '0.5rem',
                padding: '0.75rem',
                color: '#1f2937',
              },
              success: {
                style: {
                  background: '#f0fdf4',
                  border: '1px solid #bbf7d0',
                  color: '#166534',
                },
              },
              error: {
                style: {
                  background: '#fef2f2',
                  border: '1px solid #fecaca',
                  color: '#b91c1c',
                },
              },
            }} />
          </TasksProvider>
        </AuthProvider>
      </body>
    </html>
  );
}