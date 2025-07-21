import traceback

from src.main.python.com.selenium.framework.base.BasePage import BasePage
from src.main.python.com.selenium.framework.pageObjects.SwagLabs.InventoryPage import InventoryPage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    locators = {
        "userName": ("ID", "user-name"),
        "password": ("ID", "password"),
        "loginButton": ("ID", "login-button"),
        "swagLabsLogo": ("CLASS_NAME", "login_logo"),
    }

    def verify_swag_labs_login_page(self):
        self.bp_wait_for_page_to_load()
        try:
            assert self.bp_verify_url("https://www.saucedemo.com/")
            assert self.bp_get_browser_title == "Swag Labs"
            assert self.bp_is_enabled(self.userName, "Username")
            assert self.bp_is_enabled(self.password, "Password")
            assert self.bp_is_enabled(self.loginButton, "Login")
        except AssertionError:
            print("Login page verification failed")
            traceback.print_exc()
            return False
        print("Swag Labs Login Page Verified")
        return True

    def enter_username(self, username="standard_user"):
        self.bp_write_text(self.userName, username, "User Name")

    def enter_password(self, password="secret_sauce"):
        self.bp_write_text(self.password, password, "Password")

    def click_login_button(self):
        self.bp_click(self.loginButton, "Login Button")

    def login(self, username="standard_user", password="secret_sauce"):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        inventory_page: InventoryPage = InventoryPage(self.driver)
        return inventory_page
