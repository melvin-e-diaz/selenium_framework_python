# Test Execution Guide

## Quick Commands

```bash
pytest -v
pytest -v -m smoke
pytest -v -m regression
pytest -v --browser_name=edge
pytest -v --browser_name=chrome --headless=True
pytest -v --html=report.html --self-contained-html
```

## CLI Options

Defined in `src/main/python/com/selenium/framework/test/conftest.py`:

- `--browser_name` (default: `edge`)
  - Supported: `chrome`, `edge`, `firefox`, `safari`
- `--headless` (default: `False`)
  - Pass `True` for headless run in supported browsers

## Markers

Configured in `pytest.ini`:

- `smoke` - fast health checks
- `regression` - broader functional validation

Examples:

```bash
pytest -v -m smoke
pytest -v -m "smoke or regression"
pytest -v -m "not regression"
```

## Example Targeted Runs

```bash
pytest -v src/main/python/com/selenium/framework/test/test_SwagLabsLoginTest.py
pytest -v src/main/python/com/selenium/framework/test/test_SwagLabsInventoryTest.py
```

## Failure Diagnostics

Failure handling hooks attach per-phase reports and attempt screenshots for failed test calls.

Recommendations:

- keep test names explicit and stable to improve artifact traceability
- collect HTML report in CI for post-run debugging
- run single-test reproductions locally before broad reruns

## CI Execution

Workflow file: `.github/workflows/main.yml`

Pipeline behavior:

1. Install dependencies
2. Install Chrome + ChromeDriver
3. Run base smoke test file
4. Run full pytest command with HTML report output
5. Upload report artifact

## Troubleshooting

- **Driver not found**: verify expected binary path under `libs/<browser>/<platform>/`.
- **Headless issues**: try headed mode first to inspect behavior.
- **Intermittent wait failures**: prefer explicit waits in page object methods over fixed `sleep`.
