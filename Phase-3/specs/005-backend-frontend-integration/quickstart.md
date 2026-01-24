# Quickstart Guide: Backend-Frontend Integration

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
pip install fastapi uvicorn sqlmodel python-jose better-auth python-dotenv psycopg2-binary

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
# Edit NEXT_PUBLIC_API_URL to match your backend URL
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

## API Usage Examples

### Authentication
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Get user info (with JWT token)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Task Management
```bash
# Get user's tasks (replace USER_ID with actual user ID and TOKEN with JWT)
curl -X GET http://localhost:8000/api/USER_ID/tasks \
  -H "Authorization: Bearer TOKEN"

# Create a task
curl -X POST http://localhost:8000/api/USER_ID/tasks \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs"}'
```

## Testing the Integration

### Authentication Flow
1. Visit http://localhost:3000
2. Click "Sign Up" to create an account
3. Verify account creation and redirect to dashboard
4. Log in with your credentials

### Task Management Flow
1. After authentication, navigate to dashboard
2. Create a new task using the form
3. Verify the task appears in the list
4. Update, complete, or delete the task

### API Communication
1. Open browser developer tools (F12)
2. Go to Network tab
3. Perform task operations
4. Verify API calls are made with proper JWT headers
5. Check that responses match the API contract

## Troubleshooting

### Common Issues

**Issue**: Backend startup fails with import errors
**Solution**: Ensure all dependencies are installed in the virtual environment

**Issue**: CORS errors when frontend communicates with backend
**Solution**: Verify that CORS middleware allows the frontend origin (http://localhost:3000)

**Issue**: Authentication fails
**Solution**: Check that BETTER_AUTH_SECRET matches between frontend and backend

**Issue**: Database connection fails
**Solution**: Verify DATABASE_URL in backend .env file and ensure Neon Serverless is properly configured

### Verification Steps

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/
   # Should return: {"status": "ok"}
   ```

2. **CORS Configuration**:
   - Make a request from frontend origin to backend
   - Verify Access-Control-Allow-Origin header is present

3. **JWT Flow**:
   - Login and receive JWT token
   - Use JWT token in subsequent requests
   - Verify token validation works properly

4. **User Isolation**:
   - Create tasks for one user
   - Verify other users cannot access those tasks