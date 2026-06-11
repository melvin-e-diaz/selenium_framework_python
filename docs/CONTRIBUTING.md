# Contributing Guide

## Development Workflow

1. Create a feature branch from your default integration branch.
2. Implement changes in small, reviewable commits.
3. Run local tests and checks before opening a PR.
4. Document behavioral or interface changes in project docs.

## Coding Standards

- Follow PEP 8 and keep functions focused and cohesive.
- Prefer explicit type hints for new/modified public methods.
- Keep selectors inside page objects; avoid selector usage in tests.
- Add concise docstrings for new public helpers and fixtures.

## Test Standards

- Add or update tests for any functional change.
- Use pytest markers (`smoke`, `regression`) intentionally.
- Keep tests deterministic; avoid non-deterministic sleeps where possible.
- Ensure failures include actionable assertion messages.

## Page Object Standards

- One page object per functional page/region.
- Expose intent-level methods (`login`, `add_item_to_cart`) rather than low-level click chains.
- Reuse `BasePage` helper methods to keep consistency in waits/logging/error handling.

## Pull Request Checklist

- [ ] Code compiles/runs locally
- [ ] Targeted tests pass
- [ ] No unintended debug code or temporary data
- [ ] Documentation updated for user-visible changes
- [ ] CI pipeline passes

## Security and Secrets

- Do not commit real credentials, tokens, or environment secrets.
- Use environment variables for sensitive values.
- Treat sample config placeholders as non-production defaults only.
