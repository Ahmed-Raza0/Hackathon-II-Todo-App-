# Quickstart Guide: Frontend Authentication Integration

## Development Setup

### Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL (Neon Serverless)
- Git

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel python-jose[bundles] passlib[bcrypt] python-dotenv psycopg2-binary

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and JWT_SECRET
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit NEXT_PUBLIC_API_BASE to match your backend URL
```

## Running the Application

### Backend
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000

## Testing the Authentication Flow

### Registration Flow
1. Visit http://localhost:3000
2. Click "Sign Up"
3. Enter email, password (min 8 chars), and name
4. Submit form and verify account creation
5. Verify redirect to /dashboard after successful signup

### Login Flow
1. Visit http://localhost:3000
2. Click "Log In"
3. Enter your registered email and password
4. Submit form and verify successful authentication
5. Verify redirect to /dashboard after successful login

### Dashboard Access
1. After authentication, verify access to dashboard at /dashboard
2. Create, update, delete, and complete tasks
3. Verify that only your own tasks are displayed

### Route Protection
1. Attempt to access /dashboard without authentication
2. Verify redirect to /login page
3. Attempt to access /login when already authenticated
4. Verify redirect to /dashboard

## API Testing Examples

### Authentication API
```bash
# Test signup endpoint
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'

# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Test user info endpoint (with valid JWT token)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE"
```

### Task Management API
```bash
# Test fetching user's tasks (replace USER_ID with actual user ID and TOKEN with JWT)
curl -X GET http://localhost:8000/api/USER_ID/tasks \
  -H "Authorization: Bearer TOKEN"

# Test creating a task
curl -X POST http://localhost:8000/api/USER_ID/tasks \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs"}'
```

## Environment Configuration

### Backend (.env)
```
DATABASE_URL=postgresql+psycopg2://user:pass@ep-xxxxxx.us-east-1.aws.neon.tech/neondb
JWT_SECRET=50043ffe618829a82a25864b5ab0f38ed9a6c54d8f66046e85a55f2c11455296
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## Troubleshooting

### Common Issues

**Issue**: Authentication fails with 401 Unauthorized errors
**Solution**: Verify that JWT_SECRET matches between frontend and backend environments

**Issue**: CORS errors when frontend communicates with backend
**Solution**: Check that CORS_ORIGINS in backend .env includes the frontend origin (http://localhost:3000)

**Issue**: Session not persisting across page refreshes
**Solution**: Check that JWT tokens are being properly stored in localStorage and included in API requests

**Issue**: Protected routes not redirecting properly
**Solution**: Verify middleware.ts configuration and JWT token is being sent with requests

**Issue**: Database connection fails
**Solution**: Verify DATABASE_URL in backend .env file and ensure Neon Serverless PostgreSQL is properly configured

### Verification Steps

1. **JWT Flow**: Verify that tokens are properly issued during auth and attached to requests
2. **Session Management**: Check that sessions are persisted and cleared appropriately
3. **User Isolation**: Confirm that users can only access their own data
4. **Route Protection**: Test that unauthenticated access is properly blocked