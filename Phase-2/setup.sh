#!/bin/bash

echo "==========================================="
echo "Hackathon II Todo App - Setup Script"
echo "==========================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if command_exists python3; then
    echo "✓ Python 3 found: $(python3 --version)"
else
    echo "✗ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

if command_exists npm; then
    echo "✓ npm found: $(npm --version)"
else
    echo "✗ npm not found. Please install Node.js 18+"
    exit 1
fi

if command_exists docker; then
    echo "✓ Docker found: $(docker --version)"
else
    echo "⚠ Docker not found. Docker deployment will not work."
fi

if command_exists docker-compose || command_exists docker compose; then
    echo "✓ Docker Compose found"
else
    echo "⚠ Docker Compose not found. Docker deployment will not work."
fi

echo ""
echo "Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Backend dependencies installation failed"
    exit 1
fi

echo "✓ Backend dependencies installed"

echo ""
echo "Installing frontend dependencies..."
cd ../frontend
npm install

if [ $? -ne 0 ]; then
    echo "✗ Frontend dependencies installation failed"
    exit 1
fi

echo "✓ Frontend dependencies installed"

echo ""
echo "Setting up environment files..."
cd ..
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file from example"
else
    echo "- .env file already exists"
fi

if [ ! -f backend/.env ]; then
    cp .env.example backend/.env
    echo "✓ Created backend/.env file from example"
else
    echo "- backend/.env file already exists"
fi

if [ ! -f frontend/.env.local ]; then
    cp .env.example frontend/.env.local
    echo "✓ Created frontend/.env.local file from example"
else
    echo "- frontend/.env.local file already exists"
fi

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "To run the application:"
echo ""
echo "Option 1 - Separate terminals:"
echo "  Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Option 2 - Docker:"
echo "  docker-compose up --build"
echo ""
echo "Application will be available at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  Docs:     http://localhost:8000/docs"
echo ""
echo "For development, edit the .env files with your specific configuration."
echo "==========================================="