'use client';

import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils/cn';
import type { Toast as ToastType, ToastType as ToastVariant } from '@/lib/hooks/useToast';

export interface ToastProps {
  id: string;
  message: string;
  type: ToastVariant;
  onDismiss: (id: string) => void;
  duration?: number;
}

/**
 * Toast notification component
 *
 * @example
 * ```tsx
 * <Toast
 *   id="toast-1"
 *   message="Task created successfully!"
 *   type="success"
 *   onDismiss={handleDismiss}
 * />
 * ```
 */
export function Toast({ id, message, type, onDismiss, duration = 5000 }: ToastProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    // Trigger enter animation
    const enterTimer = setTimeout(() => setIsVisible(true), 10);

    // Auto-dismiss after duration
    let exitTimer: NodeJS.Timeout;
    if (duration > 0) {
      exitTimer = setTimeout(() => {
        handleDismiss();
      }, duration);
    }

    return () => {
      clearTimeout(enterTimer);
      if (exitTimer) clearTimeout(exitTimer);
    };
  }, [duration, id]);

  const handleDismiss = () => {
    setIsExiting(true);
    setTimeout(() => {
      onDismiss(id);
    }, 300); // Match exit animation duration
  };

  const variantStyles = {
    success: 'bg-green-50 border-green-500 text-green-800',
    error: 'bg-red-50 border-red-500 text-red-800',
    info: 'bg-blue-50 border-blue-500 text-blue-800',
  };

  const iconStyles = {
    success: (
      <svg
        className="h-5 w-5 text-green-500"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
          clipRule="evenodd"
        />
      </svg>
    ),
    error: (
      <svg
        className="h-5 w-5 text-red-500"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
          clipRule="evenodd"
        />
      </svg>
    ),
    info: (
      <svg
        className="h-5 w-5 text-blue-500"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
          clipRule="evenodd"
        />
      </svg>
    ),
  };

  return (
    <div
      role="alert"
      aria-live="polite"
      className={cn(
        'flex items-center gap-3 p-4 rounded-lg border-l-4 shadow-lg transition-all duration-300 max-w-md',
        variantStyles[type],
        isVisible && !isExiting
          ? 'translate-x-0 opacity-100'
          : 'translate-x-full opacity-0'
      )}
    >
      <div className="flex-shrink-0">{iconStyles[type]}</div>

      <p className="flex-1 text-sm font-medium">{message}</p>

      <button
        onClick={handleDismiss}
        className="flex-shrink-0 rounded-lg p-1 hover:bg-black/5 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-gray-500 transition-colors"
        aria-label="Dismiss notification"
      >
        <svg
          className="h-4 w-4"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>
    </div>
  );
}

/**
 * Toast container component
 * Renders multiple toasts in a fixed position
 *
 * @example
 * ```tsx
 * <ToastContainer toasts={toasts} onDismiss={dismiss} />
 * ```
 */
export function ToastContainer({
  toasts,
  onDismiss,
}: {
  toasts: ToastType[];
  onDismiss: (id: string) => void;
}) {
  if (toasts.length === 0) {
    return null;
  }

  return (
    <div
      className="fixed top-4 right-4 z-50 flex flex-col gap-3"
      aria-label="Notifications"
    >
      {toasts.map((toast) => (
        <Toast key={toast.id} {...toast} onDismiss={onDismiss} />
      ))}
    </div>
  );
}
