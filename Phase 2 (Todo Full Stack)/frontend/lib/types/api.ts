// Generic API error response
export interface APIErrorResponse {
  error: string;           // Human-readable error message
  code: string;            // Machine-readable error code (e.g., "VALIDATION_ERROR")
  details?: Record<string, string[]>; // Field-specific validation errors (optional)
}

// Custom API Error class
export class APIError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    message: string,
    public details?: Record<string, string[]>
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Error code to user-friendly message mapping
export const ERROR_MESSAGES: Record<string, string> = {
  VALIDATION_ERROR: 'Please check your input and try again.',
  INVALID_CREDENTIALS: 'Invalid email or password.',
  EMAIL_EXISTS: 'An account with this email already exists.',
  UNAUTHORIZED: 'Your session has expired. Please log in again.',
  FORBIDDEN: "You don't have permission to perform this action.",
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'Something went wrong. Please try again later.',
  NETWORK_ERROR: 'Network error. Please check your connection and try again.',
};
