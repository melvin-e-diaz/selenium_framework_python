import pytest

from src.main.python.com.selenium.framework.pageObjects.SwagLabs.LoginPage import LoginPage
from src.main.python.com.selenium.framework.utilities.JsonUtil import JsonUtil


@pytest.mark.regression
def test_SwagLabsInventoryTest(setup, file_path=None):
    _driver = setup
    test_list_item = None
    if file_path is None:
        pass
    else:
        test_list_item = JsonUtil.load_json(file_path)
    _driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(_driver)
    if test_list_item is None:
        inventory_page = login_page.login("standard_user", "secret_sauce")
    else:
        inventory_page = login_page.login(test_list_item["username"], test_list_item["password"])
    inventory_page.bp_wait_for_page_to_load()
    # inventory_page.bp_handle_alert("accept")
    assert inventory_page.verify_swag_labs_inventory_page() is True
