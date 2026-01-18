# Quickstart Guide: Backend & Frontend Boot Fix

**Feature**: 002-boot-fix
**Date**: 2026-01-16
**Status**: Draft

## Prerequisites

- Python 3.11+ (for backend)
- Node.js LTS (for frontend)
- Git

## Backend Setup and Validation

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Verify Backend Structure
Ensure the following files exist:
- `main.py` (with FastAPI app instance named 'app')
- `requirements.txt` (with fastapi and uvicorn)

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify main.py Content
Ensure main.py contains:
```python
from fastapi import FastAPI

app = FastAPI(title="Todo Phase III API")

@app.get("/health")
def health():
    return {"status": "ok"}
```

### 5. Start Backend Server
```bash
uvicorn main:app --reload --port 8000
```

### 6. Validate Backend
- Open http://127.0.0.1:8000/health
- Should return: {"status": "ok"}

## Frontend Setup and Validation

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Verify Frontend Structure
Ensure the following files exist:
- `app/page.tsx` (root page component)
- `app/layout.tsx` (root layout component)

### 3. Install Frontend Dependencies
```bash
npm install
```

### 4. Verify page.tsx Content
Ensure app/page.tsx contains:
```tsx
export default function Home() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Todo App Phase III</h1>
    </main>
  )
}
```

### 5. Start Frontend Server
```bash
npm run dev
```

### 6. Validate Frontend
- Open http://localhost:3000
- Should render the home page without 404 errors

## Integration Validation

### Running Both Servers
1. Start backend server in one terminal: `cd backend && uvicorn main:app --reload --port 8000`
2. Start frontend server in another terminal: `cd frontend && npm run dev`
3. Verify both servers run without conflicts

## Troubleshooting

### Common Backend Issues

**Issue**: "Error loading ASGI app. Could not import module 'main'"
**Solution**:
1. Verify you're in the backend directory
2. Check that main.py exists and has an 'app' variable
3. Ensure the command is run as: `uvicorn main:app --reload --port 8000`

**Issue**: Module not found errors
**Solution**: Run `pip install -r requirements.txt` to ensure dependencies are installed

### Common Frontend Issues

**Issue**: "404 – This page could not be found"
**Solution**:
1. Verify `app/page.tsx` exists in the frontend directory
2. Ensure using Next.js App Router (not Pages router)
3. Check Next.js version compatibility

## Next Steps

1. Once both servers boot successfully, proceed with Phase III development
2. Verify API communication between frontend and backend
3. Implement additional features as specified in the project requirements