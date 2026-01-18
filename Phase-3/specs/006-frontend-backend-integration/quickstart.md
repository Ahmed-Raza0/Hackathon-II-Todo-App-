# Quickstart Guide: Frontend-Backend Integration

This guide explains how the frontend-backend integration works for Add/Create operations.

## API Client Structure

The API client is located at `/frontend/src/lib/api.ts` and includes:

1. **Axios Instance**: Configured with base URL and interceptors
2. **Authentication Interceptor**: Automatically adds JWT token to requests
3. **Response Interceptor**: Handles 401 errors and redirects to login
4. **Service APIs**: Predefined endpoints for auth and tasks

## Task Creation Flow

1. **User Action**: User fills out task form and clicks "Create Task"
2. **Loading State**: Button becomes disabled, shows "Creating..." text
3. **API Call**: `taskAPI.create({ title, description })` sends POST to `/api/tasks`
4. **Token Attachment**: JWT token is automatically added via interceptor
5. **Response Handling**:
   - Success: Form clears, onTaskCreated callback refreshes task list
   - Error: Error message displays, form state preserved
6. **State Update**: UI reflects actual backend state

## Key Features

- **Automatic Authentication**: JWT tokens are attached to all requests automatically
- **Error Handling**: 401 responses trigger automatic logout and redirect
- **Loading States**: Visual feedback during API operations
- **Input Validation**: Client-side validation before API calls

## Error Scenarios

- **401 Unauthorized**: Token expired/invalid → redirect to login
- **403 Forbidden**: Permission denied → display error
- **5xx Server Error**: Backend failure → display user-friendly message
- **Network Error**: Connectivity issue → display error

## Testing the Implementation

1. Log in to the application
2. Navigate to the tasks page
3. Fill out the task form with a title and optional description
4. Click "Create Task"
5. Verify the task appears in the list after successful creation
6. Verify error handling by attempting to create a task with invalid data