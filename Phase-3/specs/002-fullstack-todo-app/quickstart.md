# Quickstart Guide: Full-Stack Todo Application

## Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL (Neon Serverless)
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel python-jose[bundles] better-auth python-dotenv

# Set up environment variables
cp .env.example .env
# Edit .env to add your DATABASE_URL and other required variables
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 4. Environment Configuration
Create `.env` files in both directories:

**Backend (.env):**
```
DATABASE_URL=postgresql+psycopg2://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname
BETTER_AUTH_SECRET=your-secret-key-here
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### 5. Run the Applications

**Backend:**
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## API Usage Examples

### Authentication
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "name": "John Doe"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
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

## Development Workflow

1. **Feature Development**: Create feature branches from main
2. **Testing**: Run backend tests with `pytest` and frontend tests with `npm test`
3. **Database Migrations**: Use SQLModel's migration system
4. **Code Style**: Follow PEP 8 for Python and ESLint standards for JavaScript

## Troubleshooting

### Common Issues

**Issue**: Cannot connect to database
**Solution**: Verify DATABASE_URL in .env file and ensure Neon Serverless is properly configured

**Issue**: JWT authentication fails
**Solution**: Check that BETTER_AUTH_SECRET matches between frontend and backend

**Issue**: Frontend cannot reach backend API
**Solution**: Ensure both applications are running and CORS is properly configured