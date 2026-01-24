# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack Todo Application built with Next.js 16+ (App Router) frontend and Python FastAPI backend, using SQLModel ORM with Neon Serverless PostgreSQL database. The project follows a monorepo architecture with Spec-Driven Development methodology using Spec-Kit Plus.

## Architecture

### Frontend (Next.js 16+ App Router)
- **Framework**: Next.js 16.1.3 with App Router
- **UI Components**: Radix UI primitives with Tailwind CSS
- **Styling**: Tailwind CSS with shadcn/ui components
- **Authentication**: Better Auth (JWT-based)
- **State Management**: React state and hooks
- **Type Safety**: TypeScript
- **Icons**: Lucide React
- **Forms**: React Hook Form with Zod validation
- **Data Visualization**: Recharts

### Backend (Python FastAPI)
- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Database Driver**: psycopg2
- **Environment**: Python virtual environment

### Project Structure
```
├── backend/
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # Database connection and engine setup
│   └── .env            # Environment variables
├── frontend/
│   ├── app/            # Next.js App Router pages
│   ├── components/     # Reusable React components
│   ├── lib/           # Utility functions
│   ├── hooks/         # Custom React hooks
│   ├── public/        # Static assets
│   ├── package.json   # Node.js dependencies
│   ├── next.config.ts # Next.js configuration
│   └── tsconfig.json  # TypeScript configuration
├── specs/             # Specification-driven development artifacts
├── history/           # Prompt History Records and ADRs
├── .specify/          # Spec-Kit Plus configuration
└── CLAUDE.md          # This file
```

## Development Commands

### Frontend Development
```bash
# Install frontend dependencies
cd frontend && npm install

# Run frontend development server
npm run dev

# Build frontend for production
npm run build

# Run frontend in production mode
npm run start

# Lint frontend code
npm run lint
```

### Backend Development
```bash
# Activate Python virtual environment
cd backend && source venv/bin/activate  # Linux/Mac
# or
cd backend && venv\Scripts\activate     # Windows

# Install Python dependencies (if needed)
pip install fastapi uvicorn sqlmodel python-dotenv

# Run backend development server
uvicorn main:app --reload

# Run backend with specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Environment Configuration
- **Backend**: Configure `DATABASE_URL` in `backend/.env`
- **Frontend**: Environment variables can be added to `frontend/.env.local`

### Common Development Tasks
```bash
# Run backend and frontend simultaneously (using tmux/screen or separate terminals)
# Terminal 1:
cd backend && uvicorn main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

## Tech Stack Details

### Frontend Technologies
- **Next.js 16.1.3**: React framework with App Router
- **React 19.2.3**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling framework
- **Better Auth**: Authentication library
- **Radix UI**: Accessible component primitives
- **Lucide React**: Icon library
- **React Hook Form**: Form management
- **Zod**: Schema validation
- **Recharts**: Data visualization

### Backend Technologies
- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL database library combining SQLAlchemy and Pydantic
- **PostgreSQL**: Relational database (Neon Serverless)
- **Pydantic**: Data validation and settings management
- **python-dotenv**: Environment variable management

## API Endpoints
- **Backend API**: `http://localhost:8000` (default)
- **Frontend App**: `http://localhost:3000` (default)
- **Health Check**: `GET /` on backend returns service status

## Testing Guidelines
- Frontend: Jest, React Testing Library (to be implemented)
- Backend: Pytest (to be implemented)
- Integration: End-to-end tests (to be implemented)

## Deployment
- **Frontend**: Vercel (recommended) or any static hosting
- **Backend**: Any Python WSGI/ASGI compatible hosting
- **Database**: Neon Serverless PostgreSQL

## Spec-Driven Development Workflow

This project uses Spec-Driven Development (SDD) methodology:

1. **Specification**: Define requirements in `specs/<feature>/spec.md`
2. **Planning**: Create architecture plan in `specs/<feature>/plan.md`
3. **Tasks**: Generate testable tasks in `specs/<feature>/tasks.md`
4. **Implementation**: Follow tasks to implement features
5. **History**: Maintain Prompt History Records in `history/prompts/`
6. **Architecture Decisions**: Document significant decisions in `history/adr/`

## Key Files and Directories

- `.specify/memory/constitution.md`: Project principles
- `specs/<feature>/spec.md`: Feature specifications
- `specs/<feature>/plan.md`: Architecture plans
- `specs/<feature>/tasks.md`: Implementation tasks
- `history/prompts/`: Prompt History Records
- `history/adr/`: Architecture Decision Records

## Special Considerations

1. **Authentication**: Using Better Auth for JWT-based authentication
2. **Database**: Neon Serverless PostgreSQL with SQLModel ORM
3. **Type Safety**: Full TypeScript support on frontend
4. **Component Library**: Using Radix UI for accessible components
5. **Environment Variables**: Keep sensitive data in .env files
6. **Monorepo**: Both frontend and backend in single repository

---

## Original Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps.

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.
