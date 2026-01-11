# Hackathon Todo - Frontend

A beautiful, responsive todo application built with Next.js 15+, TypeScript, and Tailwind CSS.

## Features

- **Authentication**: JWT-based authentication with signup/login/logout
- **Task Management**: Create, read, update, and delete tasks
- **Responsive Design**: Mobile-first design that works on all device sizes
- **Optimistic Updates**: Instant UI feedback with automatic rollback on failures
- **Loading States**: Comprehensive loading indicators and skeleton screens
- **Error Handling**: User-friendly error messages and toast notifications
- **Accessibility**: WCAG AA compliant with proper ARIA labels and keyboard navigation

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4+
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Native fetch with custom wrapper
- **Icons**: Lucide React

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the root of the frontend directory:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_APP_NAME=Hackathon Todo
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Visit [http://localhost:3000](http://localhost:3000) to see the application.

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API (e.g., http://localhost:8000)
- `NEXT_PUBLIC_APP_NAME`: Name of the application (displayed in UI)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication routes
│   ├── (dashboard)/       # Dashboard routes
│   ├── page.tsx          # Landing page
│   └── not-found.tsx     # 404 page
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components
│   ├── auth/             # Authentication components
│   └── tasks/            # Task management components
├── lib/                  # Business logic and utilities
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript type definitions
│   ├── api/              # API client and functions
│   ├── auth/             # Authentication utilities
│   └── utils/            # Utility functions
├── public/               # Static assets
└── styles/               # Global styles
```

## Key Components

- **AuthProvider**: Manages authentication state across the app
- **useTasks**: Custom hook for task management with optimistic updates
- **TaskCard**: Individual task component with edit functionality
- **TaskList**: List of tasks with empty state handling
- **Button, Input**: Reusable UI components with consistent styling
- **ToastContainer**: Global toast notification system

## API Integration

The frontend communicates with the backend API through the following endpoints:

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `PATCH /api/tasks/:id` - Update task title
- `PATCH /api/tasks/:id/toggle` - Toggle task completion
- `DELETE /api/tasks/:id` - Delete a task

## Development Guidelines

- All components are typed with TypeScript interfaces
- Form validation uses Zod schemas for type safety
- API calls are handled through a centralized client with error handling
- Authentication tokens are stored in localStorage
- Loading states are implemented with skeleton screens and spinners
- Error boundaries protect against unhandled exceptions

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is licensed under the MIT License.
