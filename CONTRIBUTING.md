# Contributing Guide

## Branching Strategy
- `main` — always deployable, protected, no direct pushes
- `feature/<short-description>` — one feature per branch
- `fix/<short-description>` — bug fixes

## Commit Convention
This project follows [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` a new feature
- `fix:` a bug fix
- `docs:` documentation only
- `refactor:` code change that neither fixes a bug nor adds a feature
- `test:` adding or correcting tests
- `chore:` tooling, dependencies, config

Example: `feat(auth): add JWT refresh token endpoint`

## Pull Requests
- Every change to `main` goes through a PR, even solo.
- PR description should state what changed and why (link the ADR if relevant).