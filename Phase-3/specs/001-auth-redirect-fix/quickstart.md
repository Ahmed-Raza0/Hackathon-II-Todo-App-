# Quickstart Guide: Auth Redirect Fix

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
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit NEXT_PUBLIC_API_BASE_URL to match your backend URL
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

### Manual Testing Steps

1. **Visit the homepage** (http://localhost:3000)
   - Unauthenticated users should see sign up/login options
   - Authenticated users should be redirected to dashboard

2. **Sign up flow**
   - Navigate to http://localhost:3000/signup
   - Enter valid email, password (min 8 chars), and name
   - Verify account creation and redirect to http://localhost:3000/dashboard

3. **Login flow**
   - Navigate to http://localhost:3000/login
   - Enter valid credentials
   - Verify successful authentication and redirect to http://localhost:3000/dashboard

4. **Dashboard access**
   - Navigate directly to http://localhost:3000/dashboard without authentication
   - Verify redirect to login page

5. **Task management**
   - On dashboard, create, update, complete, and delete tasks
   - Verify operations persist correctly

6. **Logout**
   - Click logout button on dashboard
   - Verify redirect to login page and session clearing

### API Testing

#### Authentication API
```bash
# Test auth endpoints are protected
curl -X GET http://localhost:8000/api/users/tasks \
  -H "Authorization: Bearer INVALID_TOKEN"
# Should return 401 Unauthorized

# Test with valid token
curl -X GET http://localhost:8000/api/users/tasks \
  -H "Authorization: Bearer VALID_JWT_TOKEN"
# Should return user's tasks
```

#### Environment Variables
Verify these environment variables are properly set:

**Backend (.env):**
```
DATABASE_URL=postgresql+psycopg2://user:pass@ep-xxxxxx.us-east-1.aws.neon.tech/neondb
BETTER_AUTH_SECRET=your-super-long-random-secret
JWT_SECRET=another-super-secret-for-jwt-tokens
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### Expected Behaviors

✅ Successful signup redirects to `/dashboard` (not `/api/auth/error`)
✅ Successful login redirects to `/dashboard` (not `/api/auth/error`)
✅ Failed authentication shows error message without redirecting to `/api/auth/error`
✅ Protected routes require authentication
✅ Users only see their own tasks
✅ Session persists across page refreshes
✅ Logout clears session properly

### Troubleshooting Common Issues

**Issue**: Redirecting to `/api/auth/error` instead of `/dashboard`
**Cause**: BETTER_AUTH_SECRET mismatch between frontend and backend
**Solution**: Verify both .env files have identical BETTER_AUTH_SECRET value

**Issue**: CORS errors during authentication
**Cause**: Backend not allowing credentials from frontend origin
**Solution**: Check CORS configuration in backend to allow http://localhost:3000 with credentials

**Issue**: Session not persisting across page refreshes
**Cause**: JWT token not properly stored or httpOnly cookies not configured
**Solution**: Check browser devtools for proper cookie storage and JWT handling

**Issue**: Users seeing other users' tasks
**Cause**: User ID filtering not properly implemented
**Solution**: Verify all API endpoints filter by authenticated user_id from JWT