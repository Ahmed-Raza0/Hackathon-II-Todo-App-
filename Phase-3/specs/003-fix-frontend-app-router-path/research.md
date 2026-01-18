# Research: Frontend App Router Path Resolution

**Feature**: 003-fix-frontend-app-router-path
**Date**: 2026-01-16
**Status**: Completed

## Research Findings

### Decision: Canonical Structure Adoption
**Rationale**: The SP-SRC specification mandates using `/frontend/src/app/` as the canonical location for Next.js App Router components. This eliminates routing conflicts that occur when both `/frontend/app` and `/frontend/src/app` exist simultaneously.

**Alternatives considered**:
- Keeping `/frontend/app` structure - rejected per SP-SRC-02 prohibition
- Custom structure - rejected as it violates SP-SRC-03 standard

### Decision: Migration Strategy
**Rationale**: If `/frontend/app` exists, it must be deleted and contents moved to `/frontend/src/app/` per SP-SRC-05 enforcement actions.

**Alternatives considered**:
- Symlinks - rejected as they complicate deployment and development
- Build-time copying - rejected as it adds complexity without benefit

### Decision: File Structure Validation
**Rationale**: Need to verify that both `page.tsx` and `layout.tsx` exist in the canonical location per SP-SRC-06 and SP-SRC-07 invariants.

**Validation approach**: Check for required files existence and proper exports/default components.

### Decision: Server Restart Requirement
**Rationale**: After structural changes, the development server must be restarted to pick up the new directory structure per SP-SRC-05 step 3.

**Implementation**: Include server restart instruction in implementation tasks.