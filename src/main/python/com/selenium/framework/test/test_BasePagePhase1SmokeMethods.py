from pathlib import Path
from unittest.mock import MagicMock

import pytest

from selenium_framework_python.src.main.python.com.selenium.framework.base import BasePage as basepage_module
from selenium_framework_python.src.main.python.com.selenium.framework.base.BasePage import (
    BasePage,
    DEFAULT_PERF_BUDGETS,
)


def _base_page_with_mock_driver() -> tuple[BasePage, MagicMock]:
    driver = MagicMock()
    driver.current_url = "https://example.com/home"
    driver.title = "Example Title"
    page = BasePage(driver, wait_timeout=1, highlight=False)
    return page, driver


def test_basepage_phase1_perf_and_soft_assert_smoke(tmp_path) -> None:
    page, driver = _base_page_with_mock_driver()

    driver.execute_script.return_value = {
        "ttfb": 100.0,
        "dns_lookup": 10.0,
        "tcp_connect": 20.0,
        "ssl_handshake": 8.0,
        "redirect_time": 0.0,
        "dom_content_loaded": 900.0,
        "load_complete": 1200.0,
        "first_paint": 250.0,
        "first_contentful_paint": 350.0,
    }
    nav = page.bp_capture_navigation_metrics()
    assert nav["ttfb"] == 100.0

    page.bp_perf_mark("start")
    duration = page.bp_perf_measure("measure-login", "start")
    assert duration >= 0

    with page.bp_time_action("click-login"):
        pass
    assert len(page._perf_entries) >= 2  # type: ignore[attr-defined]

    violations = page.bp_assert_performance_budgets(
        {"ttfb": 9999.0},
        budgets=DEFAULT_PERF_BUDGETS,
        soft_assertion=True,
    )
    assert violations
    soft_failures = page.bp_consume_soft_assert_failures()
    assert soft_failures
    assert page.bp_consume_soft_assert_failures() == []

    outputs = page.bp_dump_performance_report(
        artifacts_dir=tmp_path / "performance",
        test_name="phase1::perf",
        navigation_metrics=nav,
        budget_violations=violations,
    )
    assert "summary" in outputs
    assert Path(outputs["summary"]).is_file()


def test_basepage_phase1_budget_assertion_raises() -> None:
    page, _driver = _base_page_with_mock_driver()
    with pytest.raises(AssertionError):
        page.bp_assert_performance_budgets({"ttfb": 9999.0}, soft_assertion=False)


def test_basepage_phase1_bp_call_api_smoke(monkeypatch) -> None:
    page, _driver = _base_page_with_mock_driver()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"ok": True}
    mock_response.text = '{"ok": true}'
    mock_response.url = "https://example.com/api/resource"
    mock_elapsed = MagicMock()
    mock_elapsed.total_seconds.return_value = 0.123
    mock_response.elapsed = mock_elapsed
    mock_response.raise_for_status.return_value = None

    request_mock = MagicMock(return_value=mock_response)
    monkeypatch.setattr(basepage_module.requests, "request", request_mock)

    result = page.bp_call_api(
        method="GET",
        dataset_url="https://example.com/api",
        rid="resource",
        bearer_token="token123",
        params={"q": "abc"},
        description="phase1-api",
    )

    assert result["status_code"] == 200
    assert result["body"] == {"ok": True}
    assert result["url"] == "https://example.com/api/resource"
    request_mock.assert_called_once()


def test_basepage_phase1_bp_post_api_data_delegates(monkeypatch) -> None:
    page, _driver = _base_page_with_mock_driver()
    call_api_mock = MagicMock(
        return_value={
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"created": True},
            "url": "https://example.com/api/resource",
            "elapsed_ms": 12.0,
        }
    )
    monkeypatch.setattr(page, "bp_call_api", call_api_mock)

    response = page.bp_post_api_data(
        payload={"name": "item"},
        dataset_url="https://example.com/api",
        rid="resource",
        bearer_token="token123",
    )

    assert response == {"created": True}
    call_api_mock.assert_called_once()
