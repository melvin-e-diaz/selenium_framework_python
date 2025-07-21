import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.main.python.com.selenium.framework.base.BasePage import BasePage


class InventoryPage(BasePage):
    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.driver = driver

    locators = {
        "productsHeader": ("CLASS_NAME", "title"),
        "productSortDropdown": ("CLASS_NAME", "product_sort_container"),
        "inventoryItemNames": ("CLASS_NAME", "inventory_item_name "),
        "inventoryItemDescriptions": ("CLASS_NAME", "inventory_item_description"),
        "inventoryItemImages": ("CLASS_NAME", "inventory_item_img"),
        "inventoryItemPrices": ("CLASS_NAME", "inventory_item_price"),
        "inventoryItemAddToCartButtons": ("XPATH", "//button[contains(text(), 'Add to cart')]"),
        "inventoryItemRemoveFromCartButtons": ("XPATH", "//button[contains(text(), 'Remove')]"),
    }
    """
    For web elements that return multiple results, such as capturing a column, they will need to be defined like below
    so that Selenium Python can perform the necessary operations.
    """

    @property
    def inventory_item_names(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item_name ")

    @property
    def inventory_item_descriptions(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item_description")

    @property
    def inventory_item_imgs(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item_img")

    @property
    def inventory_item_prices(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")

    @property
    def inventory_item_add_to_cart_buttons(self) -> list[WebElement]:
        return self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to cart')]")

    @property
    def inventory_item_remove_from_cart_buttons(self) -> list[WebElement]:
        return self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Remove')]")

    productSortDropdownValues = ["Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"]

    def verify_swag_labs_inventory_page(self):
        self.bp_wait_for_page_to_load()
        try:
            assert self.bp_verify_url("https://www.saucedemo.com/inventory.html")
            assert self.bp_get_browser_title == "Swag Labs"
            assert self.bp_is_displayed(self.productsHeader, "Products Header")
            assert self.bp_is_enabled(self.productSortDropdown, "Products Sort")
            assert self.bp_get_all_items_from_dropdown_list(self.productSortDropdown,
                                                            "Product Sort Dropdown") == self.productSortDropdownValues
            assert self.bp_is_enabled(self.inventoryItemNames, "Inventory Item Names")
            assert self.bp_is_enabled(self.inventoryItemDescriptions, "Inventory Item Descriptions")
            assert self.bp_is_displayed(self.inventoryItemImages, "Inventory Item Images")
            assert self.bp_is_displayed(self.inventoryItemPrices, "Inventory Item Prices")
            assert self.bp_is_enabled(self.inventoryItemAddToCartButtons, "Inventory Item Add To Cart Buttons")

            # verify filters working correctly
            self.bp_select_from_dropdown_list(self.productSortDropdown, "Name (A to Z)", "Product Sort Dropdown")
            assert self.bp_verify_column_sorting(self.inventory_item_names, "asc", "Inventory Item Names")

            self.bp_select_from_dropdown_list(self.productSortDropdown, "Name (Z to A)", "Product Sort Dropdown")
            assert self.bp_verify_column_sorting(self.inventory_item_names, "desc", "Inventory Item Names")

            self.bp_select_from_dropdown_list(self.productSortDropdown, "Price (low to high)", "Product Sort Dropdown")
            assert self.bp_verify_column_sorting(self.inventory_item_prices, "asc", "Inventory Item Prices")

            self.bp_select_from_dropdown_list(self.productSortDropdown, "Price (high to low)", "Product Sort Dropdown")
            assert self.bp_verify_column_sorting(self.inventory_item_prices, "desc", "Inventory Item Prices")
        except AssertionError:
            print("Inventory Page not verified.")
            traceback.print_exc()
            return False
        print("Swag Labs Inventory Page Verified")
        return True

    def add_item_to_cart(self, item_name):
        actual_items = self.bp_get_all_items_from_dropdown_list(self.inventory_item_names)
        for index, item in enumerate(actual_items):
            if self.bp_get_text(item) == item_name:
                actual_add_to_cart_buttons = (self.bp_get_all_items_from_dropdown_list
                                              (self.inventory_item_add_to_cart_buttons))
                self.bp_click(actual_add_to_cart_buttons[index])
                return
        raise Exception("Item not found")
