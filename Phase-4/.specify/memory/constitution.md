<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.2.0
- Added sections: Containerization Rules, Kubernetes Rules, Helm Rules, AI-Assisted DevOps Governance, Environment & Secrets Policy, Validation & Acceptance Rules, Out-of-Scope Section
- Modified principles: Updated to reflect Phase IV Kubernetes deployment requirements
- Templates requiring updates: ⚠ pending review of .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Hackathon II Todo App Constitution - Phase IV

## Core Principles

### I. Phase IV Scope & Purpose
This constitution governs Phase IV only of the project; Phase IV objective is to deploy the existing Phase III Todo + AI Chatbot application on a local Kubernetes cluster using Docker, Minikube, and Helm Charts; No application feature development is allowed in this phase - only infrastructure, deployment, and DevOps automation; All deployment activities must strictly follow: sp.constitution → sp.specify → sp.plan → sp.tasks → sp.implement sequence.

### II. Application Code Freeze
Frontend (Next.js) code must remain unchanged during Phase IV; Backend (FastAPI) code must remain unchanged during Phase IV; Database schema must remain unchanged during Phase IV; Auth logic must remain unchanged during Phase IV; If something is broken, fixes must be done only via configuration, environment variables, or infrastructure changes.

### III. Single Source of Truth
Phase III code is the only valid application source; Kubernetes manifests, Helm charts, and Dockerfiles must adapt to the app, not the other way around; No modifications to application code are permitted under any circumstances.

### IV. Containerization Requirements
Frontend and Backend must be separate containers; One process per container rule must be enforced; Containers must be stateless and configured via environment variables; Database remains Neon (external managed PostgreSQL) and must not be containerized; Dockerfiles must be created for both frontend and backend services.

### V. Kubernetes Deployment Rules
Minikube is the only allowed cluster for this phase; Namespace-based isolation is required; Use only Kubernetes-native resources: Deployment, Service, ConfigMap, Secret; No hardcoded credentials inside YAML files; All configurations must be externalized via ConfigMaps or Secrets.

### VI. Helm Chart Governance
Helm is mandatory for all deployments; No raw kubectl apply -f for final deployment; Each service must be templated separately: frontend and backend; Values must be configurable via values.yaml; Helm charts must support clean install and upgrade operations.

## Security Requirements

Authentication Rules:
- Secrets Management: No secrets in Git; use Kubernetes Secrets exclusively.
- Environment Variables: All sensitive configuration must be passed via environment variables.
- Secret Types: DATABASE_URL, JWT_SECRET, BETTER_AUTH_SECRET, OPENAI keys must be stored as Kubernetes Secrets.

Configuration Rules:
- No Hardcoded URLs: No hardcoded localhost URLs inside containers; use environment variables for all endpoint configurations.
- External Dependencies: Database connections must point to Neon PostgreSQL, not local instances.

## Development Workflow

Containerization Workflow:
- Docker Image Creation: Separate Docker images for frontend and backend services.
- Multi-stage Builds: Use multi-stage builds for optimized container sizes.
- Image Tagging: Use semantic versioning for Docker image tags.
- Registry: Images stored locally for Minikube deployment.

Kubernetes Resource Management:
- Deployment Resources: Create Deployment resources for both frontend and backend.
- Service Resources: Expose services via appropriate Service types (ClusterIP, NodePort).
- Health Checks: Implement readiness and liveness probes for all deployments.
- Resource Limits: Define CPU and memory limits for all containers.

Helm Chart Development:
- Template Structure: Organize templates in proper Helm chart structure.
- Values Configuration: Parameterize all configurable aspects in values.yaml.
- Testing: Verify helm install, upgrade, and rollback operations work cleanly.
- Packaging: Package charts with proper versioning and metadata.

## AI-Assisted DevOps Governance

Docker AI (Gordon) Usage:
- Advisory Role: Gordon is advisory, not authoritative; all generated commands must be reviewed before execution.
- Fallback Strategy: Standard Docker CLI and Claude Code generated Docker commands serve as fallback when Gordon is unavailable.

kubectl-ai & kagent Usage:
- Manifest Generation: AI tools may be used to generate Kubernetes manifests.
- Debugging Support: AI tools may assist in debugging pod failures and analyzing cluster health.
- Manual Confirmation: AI must not auto-apply destructive actions; human confirmation is mandatory for deletions, scaling down to zero, and namespace removal.

## Environment & Secrets Policy

Secrets Management:
- No Git Storage: No secrets in Git; use Kubernetes Secrets exclusively.
- Conversion Process: .env files must be converted to Kubernetes Secrets.
- Secret Categories: DATABASE_URL, JWT_SECRET, BETTER_AUTH_SECRET, OPENAI keys must be properly secured.

Configuration Management:
- Environment Values: Environment-specific values must go into Helm values.yaml.
- URL Configuration: No hardcoded localhost URLs inside containers; use external configuration.

## Validation & Acceptance Rules

Deployment Success Criteria:
- ✅ Minikube cluster runs without errors
- ✅ Frontend accessible via NodePort / Ingress
- ✅ Backend API reachable from frontend
- ✅ Database connection works (Neon)
- ✅ Pods are healthy (no CrashLoopBackOff)
- ✅ Helm install / upgrade works cleanly
- ✅ App survives pod restarts

## Out-of-Scope (Explicitly Forbidden)

Prohibited Activities:
- 🚫 Cloud providers (AWS/GCP/Azure) - only Minikube allowed
- 🚫 CI/CD pipelines - manual deployment only
- 🚫 Production hardening - local development focus
- 🚫 Autoscaling (HPA) - basic deployments only
- 🚫 Service Mesh - simple networking only
- 🚫 Observability stacks (Prometheus, Grafana) - basic monitoring only

## Failure Handling Rule

Fallback Procedures:
- If Docker AI is unavailable: proceed manually using Docker CLI
- If kubectl-ai fails: use standard kubectl commands
- If kagent not supported: use manual Kubernetes operations
- In all cases: do NOT block the phase - proceed with available tools

## Governance

Amendment Procedure: Changes to this constitution must be documented with clear rationale and reviewed by project maintainers. Any architectural decision that significantly impacts deployment, security, or system architecture must be recorded in an ADR.

Versioning Policy: MAJOR for backward incompatible governance/principle removals; MINOR for new principles or material expansions (such as adding Phase IV requirements); PATCH for clarifications and typo fixes.

Compliance Review: All pull requests must be validated against this constitution. Automated checks should verify that code changes comply with the stated principles, particularly around security, deployment, and infrastructure requirements.

**Version**: 1.2.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-25