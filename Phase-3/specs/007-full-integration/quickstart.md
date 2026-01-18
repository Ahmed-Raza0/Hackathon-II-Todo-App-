# Quickstart Guide: Full Frontend-Backend Integration

## Overview
This guide explains how to set up and validate the complete frontend-backend integration for the Todo App. The integration ensures proper API communication, authentication, and build processes.

## Prerequisites
- Backend server running at http://127.0.0.1:8000
- Frontend development environment with Node.js and npm
- NEXT_PUBLIC_API_BASE_URL environment variable set to http://127.0.0.1:8000

## Setup Process

### 1. Backend Configuration
1. Ensure CORS is configured for http://localhost:3000
2. Verify health endpoint is accessible at /health
3. Confirm JWT authentication is properly implemented
4. Validate all API endpoints are under /api/* pattern

### 2. Frontend Configuration
1. Set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
2. Verify API client uses environment variable for requests
3. Confirm JWT tokens are properly attached to requests
4. Test that all API calls follow /api/* pattern

### 3. API Client Validation
1. Check that centralized API client exists at /frontend/src/lib/api.ts
2. Verify JWT token is attached to all authenticated requests
3. Test API call patterns and error handling
4. Confirm all requests go through the centralized client

## Development Workflow

### Starting Servers
1. Start backend first: `cd backend && uvicorn main:app --reload --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Access frontend at http://localhost:3000

### Testing Integration
1. Verify API calls succeed with proper authentication
2. Test task CRUD operations
3. Confirm JWT token handling works correctly
4. Validate error responses are handled appropriately

## Production Build

### Frontend Build Process
1. Run `npm run build` in the frontend directory
2. Verify no TypeScript errors occur
3. Confirm environment variables are properly used
4. Test the built application functionality

### Backend Validation
1. Run `python -m compileall .` to validate code
2. Confirm no syntax errors exist
3. Test that all endpoints are accessible
4. Verify production configuration is correct

## Validation Checklist
- [x] Backend server running at http://127.0.0.1:8000
- [x] Frontend running at http://localhost:3000
- [x] NEXT_PUBLIC_API_BASE_URL set correctly
- [x] CORS configured for frontend origin
- [x] API client properly handles JWT authentication
- [x] Task CRUD operations work end-to-end
- [x] Frontend builds successfully without errors
- [x] Backend compiles without syntax errors
- [x] Health endpoint accessible at /health
- [x] All API calls follow /api/* pattern

## Troubleshooting

### Common Issues
- **404 API Errors**: Verify NEXT_PUBLIC_API_BASE_URL is set correctly
- **CORS Errors**: Check backend CORS configuration allows http://localhost:3000
- **401 Authentication Errors**: Confirm JWT token is properly attached to requests
- **Build Failures**: Validate no TypeScript errors exist in frontend code

### Resolution Steps
1. Check environment variable configuration
2. Verify backend server is running
3. Confirm API client configuration
4. Validate JWT token handling
5. Test CORS configuration