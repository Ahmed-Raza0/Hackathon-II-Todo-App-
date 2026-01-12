@echo off
echo ===========================================
echo Hackathon II Todo App - Setup Script (Windows)
echo ===========================================

REM Check prerequisites
echo Checking prerequisites...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3 not found. Please install Python 3.9+
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
    echo ✓ Python found: %python_version%
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do set node_version=%%i
    echo ✓ Node.js found: %node_version%
)

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠ Docker not found. Docker deployment will not work.
) else (
    for /f "tokens=1,2" %%i in ('docker --version') do set docker_version=%%j
    echo ✓ Docker found: %docker_version%
)

echo.
echo Installing backend dependencies...
cd backend
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Backend dependencies installation failed
    pause
    exit /b 1
)

echo ✓ Backend dependencies installed

echo.
echo Installing frontend dependencies...
cd ..\frontend
npm install

if %errorlevel% neq 0 (
    echo ERROR: Frontend dependencies installation failed
    pause
    exit /b 1
)

echo ✓ Frontend dependencies installed

echo.
echo Setting up environment files...
cd ..
if not exist .env (
    copy .env.example .env >nul
    echo ✓ Created .env file from example
) else (
    echo - .env file already exists
)

if not exist backend\.env (
    copy .env.example backend\.env >nul
    echo ✓ Created backend/.env file from example
) else (
    echo - backend/.env file already exists
)

if not exist frontend\.env.local (
    copy .env.example frontend\.env.local >nul
    echo ✓ Created frontend/.env.local file from example
) else (
    echo - frontend/.env.local file already exists
)

echo.
echo ===========================================
echo Setup Complete!
echo ===========================================
echo.
echo To run the application:
echo.
echo Option 1 - Separate command prompts:
echo   Command Prompt 1: cd backend ^&^& call venv\Scripts\activate.bat ^&^& uvicorn main:app --reload --port 8000
echo   Command Prompt 2: cd frontend ^&^& npm run dev
echo.
echo Option 2 - Docker:
echo   docker-compose up --build
echo.
echo Application will be available at:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   Docs:     http://localhost:8000/docs
echo.
echo For development, edit the .env files with your specific configuration.
echo ===========================================
pause