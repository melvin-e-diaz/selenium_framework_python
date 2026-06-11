# Architecture Guide

## Design Goals

- Keep tests readable through Page Object Model patterns
- Centralize cross-cutting browser actions in `BasePage`
- Keep test code focused on assertions and business intent
- Support repeatable execution in local and CI environments

## Core Layers

### Test Layer

- Located under `src/main/python/com/selenium/framework/test/`
- Uses pytest functions and markers (`smoke`, `regression`)
- Relies on fixtures from `conftest.py` for setup/teardown and failure handling

### Page Object Layer

- Located under `src/main/python/com/selenium/framework/pageObjects/`
- Encapsulates selectors and page-specific interactions
- Returns page objects where appropriate to model page transitions

### Base Automation Layer

- `BasePage.py` centralizes:
  - click/type/read helpers
  - waits/synchronization
  - URL/title checks
  - cookies, windows, frames, alerts
  - optional performance collection and budget assertions
  - optional API helper methods

### Browser Bootstrap Layer

- `BrowserSetup.py` selects browser and options
- Performs platform-specific driver path resolution under `libs/`

### Configuration Layer

- `config/config.py` provides environment-specific and default config classes
- Directory bootstrap (`reports`, `screenshots`) is handled at import time

## Runtime Flow

1. `pytest` parses custom CLI options (`--browser_name`, `--headless`)
2. `setup` fixture initializes WebDriver via `BrowserSetup`
3. Test calls page objects and `BasePage` helper methods
4. On failure, hook-based artifact capture runs
5. Driver closes after each function-scoped test

## Extension Points

- Add new page objects under `pageObjects/<feature>/`
- Add reusable methods to `BasePage` with robust logging and error handling
- Add new pytest fixtures in `conftest.py` to reduce boilerplate
- Extend environment config classes in `config.py`

## Quality Practices

- Prefer explicit assertions in tests
- Keep selectors inside page objects only
- Use marker strategy to separate smoke and deeper regression coverage
- Avoid hard sleeps unless no stable synchronization primitive exists
