from typing import Optional
import pytest

from selenium_framework_python.src.main.python.com.selenium.framework.config.config import config
from selenium_framework_python.src.main.python.com.selenium.framework.pageObjects.SwagLabs.LoginPage import LoginPage
from selenium_framework_python.src.main.python.com.selenium.framework.utilities.JsonUtil import JsonUtil


@pytest.mark.smoke
def test_swag_labs_login(setup, file_path: Optional[str] = None) -> None:
    """
    Test SwagLabs login functionality.

    Args:
        setup: WebDriver fixture
        file_path: Optional path to JSON file containing test credentials
    """
    driver = setup

    # Load credentials from file or use defaults from config
    credentials = (
        JsonUtil.load_json(file_path)
        if file_path
        else config.get_user_credentials("standard")
    )

    # Navigate and verify login page
    driver.get(config.BASE_URL)
    login_page = LoginPage(driver)
    assert login_page.verify_swag_labs_login_page(), "SwagLabs login page not loaded correctly"

    # Perform login
    inventory_page = login_page.login(
        credentials["username"],
        credentials["password"]
    )
    inventory_page.bp_wait_for_page_to_load()
