# ADR 0001: Monorepo over Multi-repo

## Status
Accepted

## Context
The project consists of a Django core service, a FastAPI analytics service,
a React frontend, and infrastructure-as-code (Docker, Terraform, Nginx).
We need to decide whether these live in one repository or several.

## Decision
We will use a single monorepo containing all services and infrastructure code.

## Reasoning
- Solo-developed project: cross-service changes (e.g. a new API field consumed
  by the frontend) are common and easier to review/commit atomically in one PR.
- Module boundaries are enforced through folder structure and CI path filters
  rather than repository separation.
- Easier onboarding for reviewers (interviewers, collaborators) who can browse
  the entire system in one place.

## Consequences
- CI must use path-based triggers to avoid rebuilding unrelated services on
  every commit (addressed in Phase 15).
- If this project ever needed independent team ownership per service, a
  future migration to multi-repo would be a deliberate, documented step —
  not a default we're avoiding responsibility for.