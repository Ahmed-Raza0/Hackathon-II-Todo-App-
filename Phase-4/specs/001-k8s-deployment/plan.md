# Implementation Plan: Kubernetes Deployment (Phase IV)

**Branch**: `001-k8s-deployment` | **Date**: 2026-01-25 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy the existing Todo + AI Chatbot application to a local Kubernetes cluster using Docker, Minikube, and Helm Charts. This involves containerizing the frontend (Next.js) and backend (FastAPI) applications, creating Kubernetes resources (Deployments, Services, ConfigMaps, Secrets), and packaging everything into Helm charts for easy deployment. The plan ensures compliance with Phase IV constitutional requirements, maintaining the application code freeze while focusing solely on infrastructure and deployment automation.

## Technical Context

**Language/Version**: Dockerfile (node:18-alpine, python:3.11-slim), Kubernetes manifests (v1), Helm (v3)
**Primary Dependencies**: Docker, Minikube, kubectl, Helm, Next.js, FastAPI
**Storage**: Neon Serverless PostgreSQL (external managed database)
**Testing**: Manual verification, kubectl commands, Helm validation
**Target Platform**: Local Kubernetes cluster (Minikube)
**Project Type**: Web application (frontend/backend)
**Performance Goals**: 2 replicas for frontend, 2 replicas for backend, CPU 200m/300m, memory 256Mi/512Mi respectively
**Constraints**: Application code freeze - no changes to frontend or backend source code
**Scale/Scope**: Single namespace deployment (todo-phase4) for local development

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Phase IV Scope: Plan focuses only on deployment infrastructure, not application feature development
- ✅ Application Code Freeze: No modifications to frontend (Next.js) or backend (FastAPI) source code
- ✅ Single Source of Truth: Adapting Kubernetes manifests and Helm charts to existing Phase III code
- ✅ Containerization Requirements: Frontend and backend will be packaged in separate containers
- ✅ Kubernetes Deployment Rules: Using Minikube as the only cluster, namespace isolation, native resources
- ✅ Helm Chart Governance: Using Helm for all deployments, separate templates for frontend and backend
- ✅ Security Requirements: Secrets will be stored in Kubernetes Secrets, no hardcoded URLs
- ✅ Out-of-Scope: Sticking to Minikube only, no cloud providers or production hardening

## Project Structure

### Documentation (this feature)

```text
specs/001-k8s-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── Dockerfile                 # Created for containerization
├── .dockerignore             # Created for containerization
└── [existing FastAPI code - unchanged]

frontend/
├── Dockerfile                # Created for containerization
├── .dockerignore            # Created for containerization
└── [existing Next.js code - unchanged]

k8s/
├── helm/                     # Helm charts directory
│   ├── frontend/             # Frontend Helm chart
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       └── secret.yaml
│   └── backend/              # Backend Helm chart
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── configmap.yaml
│           └── secret.yaml
└── namespaces/               # Namespace definitions
    └── todo-phase4.yaml
```

**Structure Decision**: Following the web application structure with separate frontend and backend services. Dockerfiles will be created for both applications, and Helm charts will be created to manage the Kubernetes deployments. The existing application code remains unchanged as required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations found] | [All constitutional requirements satisfied] |