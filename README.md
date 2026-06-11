# Selenium Framework Python

Python-based UI automation framework built on Selenium WebDriver, `pytest`, and a reusable `BasePage` abstraction for robust browser and API-aware test workflows.

## Overview

This project provides:

- A reusable Selenium page abstraction in `src/main/python/com/selenium/framework/base/BasePage.py`
- Browser bootstrap and driver resolution in `src/main/python/com/selenium/framework/base/BrowserSetup.py`
- Swag Labs page objects and smoke/regression examples
- Built-in runtime artifacts for screenshots, logs, and optional performance metrics
- GitHub Actions execution via `.github/workflows/main.yml`

## Technology Stack

- Python 3.12 (CI baseline)
- `pytest`
- `selenium`
- `selenium-page-factory`
- `pytest-html`
- `openpyxl`

## Repository Structure

```text
selenium_framework_python/
|-- .github/workflows/main.yml
|-- pytest.ini
|-- requirements.txt
|-- src/main/python/com/selenium/framework/
|   |-- base/
|   |   |-- BasePage.py
|   |   `-- BrowserSetup.py
|   |-- config/config.py
|   |-- pageObjects/SwagLabs/
|   `-- test/
|       |-- conftest.py
|       |-- test_SwagLabsLoginTest.py
|       `-- test_SwagLabsInventoryTest.py
`-- docs/
```

## Prerequisites

- Python 3.10+ (3.12 recommended)
- Browser(s) you plan to automate (Chrome/Edge/Firefox/Safari)
- Matching browser drivers stored under `libs/<browser>/<platform>/`
- `pip` available on path

## Local Setup

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Validate driver layout

`BrowserSetup` expects drivers in:

- `libs/chrome/windows/chromedriver.exe` (Windows example)
- `libs/edge/windows/msedgedriver.exe`
- `libs/firefox/windows/geckodriver.exe`

Equivalent non-Windows binaries should exist in `linux` or `mac` platform folders.

## Running Tests

### Default run

```bash
pytest -v
```

### Browser selection

```bash
pytest -v --browser_name=edge
pytest -v --browser_name=chrome
pytest -v --browser_name=firefox
```

### Headless execution

```bash
pytest -v --browser_name=chrome --headless=True
```

### Marker-based execution

```bash
pytest -v -m smoke
pytest -v -m regression
```

### HTML report

```bash
pytest -v --html=report.html --self-contained-html
```

## Test Configuration

Global configuration is located at `src/main/python/com/selenium/framework/config/config.py`:

- `BASE_URL`
- test user credentials (`TEST_USERS`)
- wait and timeout settings
- screenshot and logging defaults
- environment profile mapping (`development`, `staging`, `production`, `default`)

Environment variable overrides include:

- `TEST_ENV`
- `BROWSER`
- `HEADLESS`
- `LOG_LEVEL`
- `STAGING_URL` / `PROD_URL`

## Fixtures and Artifacts

`src/main/python/com/selenium/framework/test/conftest.py` provides:

- custom CLI args (`--browser_name`, `--headless`)
- `setup` fixture for driver lifecycle
- failure hooks and screenshot capture behavior

By default, screenshot filenames are generated from the pytest node id and timestamp.

## CI/CD

The GitHub Actions workflow:

- installs Python 3.12 dependencies
- installs Chrome + ChromeDriver on Ubuntu
- runs smoke and full pytest suites
- uploads `report.html` as an artifact

See `.github/workflows/main.yml` for exact commands.

## Documentation Index

- `PORTFOLIO.md`
- `docs/ARCHITECTURE.md`
- `docs/TEST_EXECUTION.md`
- `docs/CONTRIBUTING.md`

## Known Constraints

- Safari headless mode is not supported by Selenium/WebDriver.
- Driver binaries must be present at expected paths; otherwise startup fails.
- Credentials in `config.py` are sample defaults for Swag Labs and should not be treated as secure secrets.
