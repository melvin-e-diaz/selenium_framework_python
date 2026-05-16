from pathlib import Path
from unittest.mock import MagicMock

from selenium.webdriver.common.by import By

from selenium_framework_python.src.main.python.com.selenium.framework.base.BasePage import BasePage


def _base_page_with_mock_driver() -> tuple[BasePage, MagicMock]:
    driver = MagicMock()
    driver.current_url = "https://example.com/home"
    driver.title = "Example Title"
    page = BasePage(driver, wait_timeout=1, highlight=False)
    return page, driver


def test_basepage_observability_and_tracing_smoke(tmp_path, monkeypatch) -> None:
    page, driver = _base_page_with_mock_driver()

    monkeypatch.setenv("PW_ARTIFACTS_DIR", str(tmp_path / "artifacts_env"))
    assert page.bp_artifacts_root() == Path(tmp_path / "artifacts_env")

    page.bp_attach_runtime_listeners()
    driver.get_log.return_value = [{"level": "INFO", "message": "console ok"}]
    outputs = page.bp_dump_runtime_logs(tmp_path / "runtime", "smoke::basepage")
    assert set(outputs.keys()) == {"console", "pageerror", "requestfailed", "meta"}
    assert Path(outputs["meta"]).is_file()

    page.bp_start_tracing(name="smoke_trace")
    trace_path = page.bp_stop_tracing(tmp_path / "trace" / "trace_meta.json")
    assert trace_path is not None
    assert Path(trace_path).is_file()


def test_basepage_verification_helpers_smoke() -> None:
    page, driver = _base_page_with_mock_driver()
    del driver  # driver is intentionally unused in this test

    page.bp_get_text = MagicMock(side_effect=["Hello World", "10.50", "10.55"])  # type: ignore[method-assign]
    assert page.bp_verify_text_contains("ignored", "World", case_sensitive=True)

    page.bp_get_text = MagicMock(side_effect=["10.50", "10.55"])  # type: ignore[method-assign]
    assert page.bp_is_equal("left", "right", tolerance=0.1)


def test_basepage_locator_cookie_and_screenshot_smoke(tmp_path) -> None:
    page, driver = _base_page_with_mock_driver()

    driver.find_elements.return_value = [MagicMock(), MagicMock()]
    assert page.bp_verify_element_count((By.CSS_SELECTOR, ".item"), expected_count=2)

    driver.get_cookie.return_value = {"name": "session", "value": "abc123"}
    cookie = page.bp_get_cookie("session")
    assert cookie and cookie["value"] == "abc123"
    page.bp_set_cookie({"name": "session", "value": "xyz"})
    page.bp_clear_cookies()
    driver.add_cookie.assert_called_once()
    driver.delete_all_cookies.assert_called_once()

    screenshot_path = tmp_path / "screenshots" / "smoke.png"
    out = page.bp_take_screenshot(file_path=str(screenshot_path))
    assert out == str(screenshot_path)
    driver.save_screenshot.assert_called_once_with(str(screenshot_path))
