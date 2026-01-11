# Environment Configuration Guide

## Frontend Environment Variables

### Required Variables
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL (e.g., `http://localhost:8000` for development or production backend URL)
- `NEXT_PUBLIC_APP_NAME` - Application name (default: "Hackathon Todo")

### Setup Instructions
1. Create a `.env.local` file in the `frontend/` directory
2. Add the required variables:
```bash
# Backend API Base URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# App Configuration
NEXT_PUBLIC_APP_NAME=Hackathon Todo
```

## Backend Environment Variables

### Required Variables
- `DATABASE_URL` - Database connection string (e.g., PostgreSQL URL)
- `BETTER_AUTH_SECRET` - Secret key for authentication
- `BETTER_AUTH_URL` - Authentication service URL

### Setup Instructions
1. Create a `.env` file in the `backend/` directory
2. Add the required variables:
```bash
DATABASE_URL=your_database_connection_string
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=your_auth_url
```

## Deployment Configuration

### Vercel Frontend Deployment
When deploying to Vercel, set the environment variables in the Vercel dashboard or using the CLI:
```bash
vercel env add NEXT_PUBLIC_API_BASE_URL production
```

### Backend Cloud Deployment
For backend deployment (AWS, GCP, Azure, Railway, Render, etc.), set the environment variables in your cloud provider's dashboard or deployment configuration.

## Environment-Specific Values

### Development
- Frontend: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
- Backend: Local database URL and development secrets

### Production
- Frontend: `NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com`
- Backend: Production database URL and production secrets