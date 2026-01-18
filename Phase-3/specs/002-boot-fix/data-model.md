# Data Model: Backend & Frontend Boot Fix

**Feature**: 002-boot-fix
**Date**: 2026-01-16
**Status**: N/A

## Entities

### Backend App
**Description**: FastAPI application instance that must be accessible as 'app' in main.py
- `app`: FastAPI instance (required for uvicorn to load)

### Frontend Page
**Description**: Next.js root page component that must exist in the App Router structure
- `page.tsx`: Root page component (required for frontend boot)

## Database Schema

N/A - This is a structural fix, not involving database changes.

## Relationships

N/A - This is a structural fix, not involving data relationships.