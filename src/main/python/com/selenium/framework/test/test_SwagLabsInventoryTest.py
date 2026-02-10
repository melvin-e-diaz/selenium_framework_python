"""
Optimized SwagLabs Test Suite
"""
from typing import Optional, Dict
import pytest
from selenium_framework_python.src.main.python.com.selenium.framework.config.config import config
from selenium_framework_python.src.main.python.com.selenium.framework.pageObjects.SwagLabs.LoginPage import LoginPage
from selenium_framework_python.src.main.python.com.selenium.framework.utilities.JsonUtil import JsonUtil


# ============================================================================
# FIXTURES
# ============================================================================
@pytest.fixture
def credentials(request) -> Dict[str, str]:
    """
    Fixture to load test credentials from file or use defaults.

    Usage:
        @pytest.mark.parametrize("credentials", ["path/to/creds.json"], indirect=True)
        def test_example(credentials):
            ...
    """
    file_path = getattr(request, 'param', None)

    if file_path:
        return JsonUtil.load_json(file_path)
    return config.get_user_credentials("standard")


@pytest.fixture
def authenticated_inventory_page(setup, credentials):
    """
    Fixture that handles login and returns inventory page.
    Reduces boilerplate code in tests.
    """
    driver = setup
    driver.get(config.BASE_URL)

    login_page = LoginPage(driver)
    assert login_page.verify_swag_labs_login_page(), "Login page verification failed"

    inventory_page = login_page.login(
        credentials["username"],
        credentials["password"]
    )
    inventory_page.bp_wait_for_page_to_load()

    return inventory_page


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def perform_login(driver, credentials: Dict[str, str]):
    """
    Helper function to perform login operation.

    Args:
        driver: WebDriver instance
        credentials: Dictionary with 'username' and 'password' keys

    Returns:
        InventoryPage instance
    """
    driver.get(config.BASE_URL)
    login_page = LoginPage(driver)

    inventory_page = login_page.login(
        credentials["username"],
        credentials["password"]
    )
    inventory_page.bp_wait_for_page_to_load()

    return inventory_page


# ============================================================================
# TESTS
# ============================================================================

@pytest.mark.smoke
def test_swag_labs_login(setup, file_path: Optional[str] = None) -> None:
    """
    Test SwagLabs login functionality.

    Args:
        setup: WebDriver fixture
        file_path: Optional path to JSON file containing test credentials
    """
    driver = setup
    credentials = (
        JsonUtil.load_json(file_path)
        if file_path
        else config.get_user_credentials("standard")
    )

    login_page = LoginPage(driver)
    driver.get(config.BASE_URL)

    assert login_page.verify_swag_labs_login_page(), "Login page verification failed"

    inventory_page = login_page.login(
        credentials["username"],
        credentials["password"]
    )
    inventory_page.bp_wait_for_page_to_load()


@pytest.mark.regression
def test_swag_labs_inventory(setup, file_path: Optional[str] = None) -> None:
    """
    Test SwagLabs inventory page display and functionality.

    Args:
        setup: WebDriver fixture
        file_path: Optional path to JSON file containing test credentials
    """
    driver = setup
    credentials = (
        JsonUtil.load_json(file_path)
        if file_path
        else config.get_user_credentials("standard")
    )

    # Perform login
    inventory_page = perform_login(driver, credentials)

    # Verify inventory page loaded correctly
    assert inventory_page.verify_swag_labs_inventory_page(), \
        "Inventory page verification failed"
