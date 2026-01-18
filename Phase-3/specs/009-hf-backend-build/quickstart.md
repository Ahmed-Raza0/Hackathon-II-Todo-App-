# Quickstart Guide: Hugging Face Backend Deployment

## Overview
This guide explains how to prepare and deploy the FastAPI backend to Hugging Face Spaces following the SP-BACKEND-HF-BUILD specification.

## Prerequisites
- Repository with the backend code in `/backend` directory
- main.py file at repository root exposing the 'app' variable
- requirements.txt with all necessary dependencies
- All secrets configured as environment variables

## Required Files Structure
```
/repository-root
 ├── main.py              # Hugging Face entry point (exposes 'app')
 ├── requirements.txt     # Dependencies for Hugging Face build
 ├── README.md           # Documentation
 └── backend/            # Source code directory
     ├── src/
     │   ├── main.py     # Original backend implementation
     │   └── ...
     └── ...
```

## Configuration Steps

### 1. Verify Runtime Entry Point
Ensure `/main.py` exists with proper FastAPI app exposure:
```python
from backend.src.main import app  # Import the main FastAPI app

# The app variable is now available for Hugging Face to serve
```

Or alternatively, ensure the root main.py contains the complete app implementation that exposes the 'app' variable.

### 2. Check Dependencies
Verify `/requirements.txt` includes all necessary packages:
- fastapi
- uvicorn
- pydantic
- sqlmodel
- python-dotenv
- Any other required packages

### 3. Environment Variables Setup
Configure environment variables in Hugging Face Space settings:
- DATABASE_URL
- BETTER_AUTH_SECRET
- OPENAI_API_KEY (if needed)

### 4. Port Configuration
Ensure no hardcoded ports exist in the application - Hugging Face assigns ports automatically.

## Deployment Process

### Step 1: Repository Preparation
1. Ensure main.py is at repository root level
2. Verify requirements.txt contains all dependencies
3. Confirm no hardcoded secrets exist in source code
4. Test locally with environment variables

### Step 2: Hugging Face Space Creation
1. Create new Space on Hugging Face
2. Select "Python" SDK
3. Set Python version to 3.10
4. Point App File to `main.py`
5. Add environment variables in Space settings

### Step 3: Verification
1. Monitor build logs for any errors
2. Verify the application starts successfully
3. Test API endpoints to ensure functionality
4. Confirm authentication and task operations work

## Common Issues and Solutions

### Issue: Build Fails to Start
**Symptoms**: No build process begins in Hugging Face
**Solution**:
- Verify main.py exists at repository root
- Confirm 'app' variable is exposed in main.py
- Check that main.py doesn't have syntax errors

### Issue: App Crashes After Build
**Symptoms**: Build succeeds but application crashes
**Solution**:
- Check for hardcoded ports or uvicorn.run() calls
- Verify all dependencies are in requirements.txt
- Confirm environment variables are properly configured

### Issue: Module Not Found
**Symptoms**: ImportError during startup
**Solution**:
- Verify import paths are correct relative to repository root
- Check that all required packages are in requirements.txt
- Ensure relative imports work correctly in Hugging Face environment

### Issue: Authentication Problems
**Symptoms**: JWT authentication fails or secrets not accessible
**Solution**:
- Verify environment variables are set in Hugging Face Space settings
- Confirm secrets are read from os.environ, not hardcoded
- Check that BETTER_AUTH_SECRET matches between frontend and backend

## Validation Checklist
- [x] main.py exists at repository root
- [x] 'app' variable is exposed in main.py
- [x] requirements.txt includes all dependencies
- [x] No hardcoded secrets in source code
- [x] Environment variables properly configured in Hugging Face
- [x] No hardcoded port bindings
- [x] Build completes successfully on Hugging Face
- [x] API endpoints respond correctly
- [x] Authentication flow works properly
- [x] Task operations function as expected