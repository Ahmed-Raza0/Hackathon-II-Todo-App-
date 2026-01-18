# Quickstart Guide: Full-Stack Todo Web App

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-16
**Status**: Draft

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL (or Neon PostgreSQL account)
- Better Auth account/configuration
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-app
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration

Create `.env` files in both backend and frontend directories:

**Backend (.env)**:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3000
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 5. Database Setup
```bash
cd backend
python -m alembic upgrade head  # Run database migrations
```

### 6. Run the Applications

**Backend**:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm run dev
```

## Development Commands

### Backend
- Run tests: `pytest`
- Run with auto-reload: `uvicorn main:app --reload`
- Run linter: `flake8 .` and `black .`

### Frontend
- Development server: `npm run dev`
- Build for production: `npm run build`
- Run tests: `npm run test`
- Run linter: `npm run lint`

## API Testing

Once both applications are running:

1. Navigate to `http://localhost:3000` to access the frontend
2. Register a new account or log in
3. Create tasks via the UI or directly through the API at `http://localhost:8000/api/tasks`

## Troubleshooting

### Common Issues

**Issue**: Database connection fails
**Solution**: Verify DATABASE_URL in backend/.env and ensure PostgreSQL is running

**Issue**: Authentication not working
**Solution**: Ensure BETTER_AUTH_SECRET is the same in both frontend and backend environments

**Issue**: Frontend can't connect to backend API
**Solution**: Verify NEXT_PUBLIC_API_BASE_URL in frontend/.env.local points to the correct backend URL

## Next Steps

1. Implement the full feature set as outlined in the specification
2. Add comprehensive tests for all components
3. Set up CI/CD pipeline
4. Deploy to staging environment for further testing