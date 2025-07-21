import traceback

from src.main.python.com.selenium.framework.base.BasePage import BasePage


class Header(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    locators = {
        "hamburgerMenu": ("ID", "react-burger-menu-btn"),
        "hamburgerMenu_AllItems": ("LINK_TEXT", "All Items"),
        "hamburgerMenu_About": ("LINK_TEXT", "About"),
        "hamburgerMenu_Logout": ("LINK_TEXT", "Logout"),
        "hamburgerMenu_ResetAppState": ("LINK_TEXT", "Reset App State"),
        "hamburgerMenu_Close": ("ID", "react-burger-cross-btn"),
        "swagLabsLogo": ("CLASS_NAME", "app_logo"),
        "shoppingCart": ("CLASS_NAME", "shopping_cart_link"),
    }

    def verify_swag_labs_header(self):
        try:
            assert self.bp_is_enabled(self.hamburgerMenu, "Hamburger Menu")
            assert self.bp_is_displayed(self.swagLabsLogo, "Logo")
            assert self.bp_is_enabled(self.shoppingCart, "Shopping Cart")

            self.bp_click(self.hamburgerMenu, "Hamburger Menu")

            assert self.bp_is_enabled(self.hamburgerMenu_AllItems, "All Items")
            assert self.bp_is_enabled(self.hamburgerMenu_About, "About")
            assert self.bp_is_enabled(self.hamburgerMenu_Logout, "Logout")
            assert self.bp_is_enabled(self.hamburgerMenu_ResetAppState, "Reset App State")
            assert self.bp_is_enabled(self.hamburgerMenu_Close, "Close")

            self.bp_click(self.hamburgerMenu_Close, "Hamburger Menu_Close")
        except AssertionError:
            print("Header not verified.")
            traceback.print_exc()
            return False
        print("Swag Labs Header Verified")
        return True

    def click_hamburger_menu_link(self, hyperlink_text):
        self.bp_click(self.hamburgerMenu, "Hamburger Menu")
        match hyperlink_text:
            case "About":
                self.bp_click(self.hamburgerMenu_About, "About")
            case "Logout":
                self.bp_click(self.hamburgerMenu_Logout, "Logout")
            case "Reset App State":
                self.bp_click(self.hamburgerMenu_ResetAppState, "Reset App State")
            case "All Items":
                self.bp_click(self.hamburgerMenu_AllItems, "All Items")
            case _:
                raise Exception(f"Invalid Link text: {hyperlink_text}")

    def click_shopping_cart_link(self):
        self.bp_click(self.shoppingCart, "Shopping Cart")
