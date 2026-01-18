# Research: Backend & Frontend Boot Fix

**Feature**: 002-boot-fix
**Date**: 2026-01-16
**Status**: Completed

## Research Findings

### Decision: Backend Structure Verification
**Rationale**: The SP-FIX specification requires a specific backend structure with main.py exposing an 'app' variable for FastAPI. This resolves the "Error loading ASGI app. Could not import module 'main'" issue.

**Alternatives considered**:
- Alternative entrypoint names - rejected as SP-FIX mandates main.py
- Different ASGI servers - rejected as FastAPI with uvicorn is specified

### Decision: Frontend Structure Verification
**Rationale**: The SP-FIX specification requires a specific frontend structure with Next.js App Router and a root page at app/page.tsx. This resolves the "404 – This page could not be found" issue.

**Alternatives considered**:
- Pages router instead of App router - rejected as SP-FIX mandates App router
- Different file names/extensions - rejected as SP-FIX specifies exact locations

### Decision: Uvicorn Execution Command
**Rationale**: The SP-FIX specification mandates using "uvicorn main:app --reload --port 8000" from the /backend directory. This ensures proper module resolution.

### Decision: Dependency Verification
**Rationale**: Ensuring FastAPI and uvicorn are properly installed in the backend environment is critical for resolving import errors.

### Decision: Health Endpoint Validation
**Rationale**: The SP-FIX specification requires a health endpoint at /health that returns {"status": "ok"}. This validates successful backend boot.