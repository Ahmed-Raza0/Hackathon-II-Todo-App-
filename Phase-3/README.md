# Full-Stack Todo Web App

A secure, multi-user todo web application using Next.js/TypeScript for frontend and FastAPI/SQLModel for backend. The system leverages Better Auth for JWT-based authentication and Neon PostgreSQL for persistent storage. Key features include user registration/login, secure task CRUD operations, and data isolation between users.

## Features

- User registration and authentication
- Secure task management (Create, Read, Update, Delete)
- User isolation - users can only access their own tasks
- JWT-based authentication
- Responsive UI with Next.js App Router
- Clean, modern UI with Tailwind CSS

## Tech Stack

- **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth with JWT tokens
- **Styling**: Tailwind CSS

## Project Structure

```
todo-app/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   ├── routes/
│   │   ├── core/
│   │   ├── middleware/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── context/
│   │   ├── styles/
│   │   └── types/
│   └── package.json
├── specs/
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL (or Neon PostgreSQL account)
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with the following content:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
   SECRET_KEY=your-super-secret-key-change-this
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Run the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the frontend directory with the following content:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`.

## API Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate a user
- `GET /api/users/me` - Get current user profile
- `GET /api/tasks` - Get all tasks for the current user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `PATCH /api/tasks/{task_id}/complete` - Mark a task as completed
- `DELETE /api/tasks/{task_id}` - Delete a task

## Development

### Backend Development

- Run tests: `pytest`
- Run with auto-reload: `uvicorn src.main:app --reload`
- Format code: `black .`
- Lint code: `flake8 .`

### Frontend Development

- Development server: `npm run dev`
- Build for production: `npm run build`
- Run tests: `npm run test`
- Lint code: `npm run lint`

## Security

- JWT-based authentication ensures stateless sessions
- User data isolation prevents cross-user access
- Passwords are hashed using bcrypt
- Input validation is performed on both frontend and backend