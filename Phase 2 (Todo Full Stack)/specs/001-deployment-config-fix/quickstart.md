# Quickstart Guide: Production Deployment Configuration Fix

## Overview
This guide provides step-by-step instructions to fix the deployment, configuration, and integration issues in the full-stack Todo application. The fixes ensure proper Tailwind CSS rendering, frontend-backend communication, and environment variable handling.

## Prerequisites
- Node.js 18+ (for frontend)
- npm or yarn
- Python 3.9+ (for backend)
- PostgreSQL database (local or hosted)
- Git

## Frontend Setup (Next.js 16 on Vercel)

### 1. Environment Configuration
Create or update `.env.local` in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com
NEXT_PUBLIC_APP_NAME=Hackathon Todo
```

For Vercel deployment, add these environment variables in the Vercel dashboard:
- `NEXT_PUBLIC_API_BASE_URL`: Your backend production URL
- `NEXT_PUBLIC_APP_NAME`: Your application name

### 2. Tailwind CSS Configuration
Verify `tailwind.config.ts` includes the App Router paths:
```ts
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  // ... rest of config
}
```

### 3. Build and Deploy to Vercel
```bash
# Install dependencies
npm install

# Build the application
npm run build

# Deploy to Vercel (or connect GitHub repo to Vercel dashboard)
npx vercel --prod
```

## Backend Setup (FastAPI)

### 1. Environment Configuration
Create `.env` file in the backend root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
ALLOWED_ORIGINS=https://your-vercel-domain.vercel.app,http://localhost:3000
PORT=8000
ENVIRONMENT=development
```

For production deployment, set these environment variables in your hosting environment.

### 2. Install Dependencies
```bash
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-dotenv sqlmodel
```

### 3. Run the Application
For development:
```bash
uvicorn main:app --reload --port 8000
```

For production:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Environment-Specific Configuration

### Local Development
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- CORS: Allow `http://localhost:3000`

### Production
- Frontend: Your Vercel domain (e.g., `https://your-app.vercel.app`)
- Backend: Your backend domain (e.g., `https://your-backend.onrender.com`)
- CORS: Allow only production domains

## Common Deployment Issues and Solutions

### 1. Tailwind CSS Not Working in Production
**Issue**: Styles appear broken in Vercel deployment
**Solution**:
- Verify content paths in `tailwind.config.ts` include App Router structure
- Check that global CSS is imported in `app/layout.tsx`
- Ensure no dynamic class names break Tailwind's purge process

### 2. API Requests Failing in Production
**Issue**: Frontend can't communicate with backend in production
**Solution**:
- Confirm `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Verify CORS configuration allows your frontend domain
- Check that backend is accessible from internet

### 3. CORS Errors
**Issue**: Browser blocks requests due to CORS policy
**Solution**:
- Update backend CORS middleware to include your production domain
- Ensure Authorization header is allowed for JWT requests
- Verify preflight OPTIONS requests are handled

### 4. Authentication Failures
**Issue**: JWT authentication fails in production
**Solution**:
- Confirm JWT secret is consistent between environments
- Verify token storage and retrieval mechanisms
- Check that authentication endpoints are accessible

## Testing the Fix

### 1. Frontend Tests
```bash
# Run frontend tests
npm test

# Check Tailwind classes
npm run build
```

### 2. Backend Tests
```bash
# Run backend tests
python -m pytest tests/
```

### 3. End-to-End Tests
1. Navigate to your frontend URL
2. Verify styling appears correctly
3. Sign up/create account
4. Create and manage tasks
5. Verify all functionality works as expected

## Deployment Checklist

- [ ] Tailwind CSS applies correctly in production
- [ ] Frontend and backend communicate properly
- [ ] CORS configuration allows frontend domain
- [ ] Environment variables configured for each environment
- [ ] Authentication works end-to-end
- [ ] API requests succeed in production
- [ ] Error handling displays properly
- [ ] All functionality works as expected

## Troubleshooting

### Frontend Build Issues
- Clear Next.js cache: `rm -rf .next`
- Verify Node.js version compatibility
- Check environment variable prefixes (must use NEXT_PUBLIC_*)

### Backend Startup Issues
- Verify environment variables are loaded
- Check database connection string format
- Confirm Uvicorn configuration for production

### Network Communication Issues
- Verify firewall settings
- Check if backend is publicly accessible
- Confirm URL schemes (http vs https) match

## Rollback Plan
If deployment fails:
1. Revert environment variables to previous values
2. Redeploy previous stable version
3. Monitor logs for error patterns
4. Apply fixes incrementally