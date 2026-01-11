# Deployment Process and Troubleshooting Guide

## Deployment Process

### Frontend (Next.js) Deployment to Vercel
1. Ensure all environment variables are configured in Vercel dashboard:
   - `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (e.g., https://your-backend.onrender.com)
   - `NEXT_PUBLIC_APP_NAME`: Application name

2. Deploy using Vercel CLI or GitHub integration:
   ```bash
   vercel --prod
   ```

3. Verify the deployment by accessing the frontend URL

### Backend (FastAPI) Deployment
1. Set up environment variables in your cloud provider:
   - `DATABASE_URL`: PostgreSQL database connection string
   - `BETTER_AUTH_SECRET`: Authentication secret key
   - `BETTER_AUTH_URL`: Authentication service URL

2. Deploy using your preferred cloud provider (Render, Railway, AWS, etc.)

3. Verify the backend is accessible at the configured URL

## Configuration Requirements

### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Must point to your deployed backend
- Should use HTTPS in production

### Backend Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Strong secret key for JWT signing
- `BETTER_AUTH_URL`: Backend URL for auth redirects

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Frontend shows unstyled UI (Tailwind CSS not working)
- **Symptom**: UI appears unstyled with no colors or layout
- **Cause**: Tailwind classes not properly processed in production
- **Solution**:
  - Verify `tailwind.config.ts` includes all necessary content paths:
    ```js
    content: [
      './app/**/*.{js,ts,jsx,tsx,mdx}',
      './components/**/*.{js,ts,jsx,tsx,mdx}',
      './lib/**/*.{js,ts,jsx,tsx,mdx}',
      './styles/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    ```
  - Ensure PostCSS configuration is correct
  - Run `npm run build` locally to test

#### 2. API requests failing between frontend and backend
- **Symptom**: Network errors when making API calls
- **Cause**: CORS configuration or URL mismatch
- **Solution**:
  - Verify `NEXT_PUBLIC_API_BASE_URL` points to correct backend URL
  - Check backend CORS configuration includes frontend domain
  - Ensure both services use HTTPS in production
  - Verify Authorization header is allowed in CORS

#### 3. Authentication issues
- **Symptom**: Login fails or user gets logged out unexpectedly
- **Cause**: JWT validation or token storage issues
- **Solution**:
  - Verify `BETTER_AUTH_SECRET` is consistent between services
  - Check that tokens are properly stored in localStorage
  - Ensure JWT has proper expiration time
  - Verify user_id validation in API routes

#### 4. Backend startup errors
- **Symptom**: Backend fails to start with import or configuration errors
- **Solution**:
  - Verify all environment variables are set
  - Check database connection string format
  - Ensure all dependencies are installed
  - Verify middleware configuration

#### 5. Database connection issues
- **Symptom**: Database operations fail with connection errors
- **Solution**:
  - Verify `DATABASE_URL` is correctly formatted
  - Check database credentials and permissions
  - Ensure database is accessible from deployment environment
  - Verify SSL requirements for production databases

### Health Checks

#### Frontend Health Check
- Access the deployed frontend URL
- Verify styling is applied correctly
- Test navigation between pages
- Verify API calls work (login, create task, etc.)

#### Backend Health Check
- Access `/health` endpoint: `GET /health`
- Should return: `{"status": "healthy"}`
- Access root endpoint: `GET /`
- Should return: `{"message": "Todo Backend API"}`

### Monitoring and Logging

#### Frontend
- Monitor browser console for JavaScript errors
- Check network tab for failed API requests
- Verify proper error handling displays to users

#### Backend
- Monitor application logs for errors
- Check database connection stability
- Monitor API response times
- Verify authentication token validation

### Rollback Procedures

If issues occur after deployment:

#### Frontend Rollback
1. Use Vercel's deployment history to revert to previous version
2. Or redeploy a known working commit

#### Backend Rollback
1. Revert to previous version in your cloud provider
2. Or redeploy a known working commit

### Performance Considerations

- Monitor bundle sizes for the frontend
- Optimize database queries if response times are slow
- Consider caching strategies for frequently accessed data
- Monitor concurrent user capacity

### Security Best Practices

- Use strong, unique secrets for `BETTER_AUTH_SECRET`
- Enable HTTPS for all production deployments
- Regularly rotate secrets
- Monitor for suspicious authentication attempts
- Keep dependencies updated

## Verification Checklist

Before marking deployment as successful:

- [ ] Frontend builds successfully
- [ ] Backend starts without errors
- [ ] Health checks pass on both services
- [ ] Frontend can communicate with backend API
- [ ] Authentication flow works end-to-end
- [ ] All CRUD operations work for tasks
- [ ] Styling appears correctly in frontend
- [ ] Error handling displays properly
- [ ] Mobile responsiveness verified
- [ ] Security headers are properly set