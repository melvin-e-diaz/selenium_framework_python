import traceback
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_framework_python.src.main.python.com.selenium.framework.base.BasePage import BasePage
from selenium_framework_python.src.main.python.com.selenium.framework.config.config import config


class InventoryPage(BasePage):
    # Expected page properties
    EXPECTED_URL = f"{config.BASE_URL}inventory.html"
    EXPECTED_TITLE = "Swag Labs"

    # Sort options
    SORT_OPTIONS = {
        "name_asc": "Name (A to Z)",
        "name_desc": "Name (Z to A)",
        "price_asc": "Price (low to high)",
        "price_desc": "Price (high to low)"
    }

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize InventoryPage.

        Args:
            driver: WebDriver instance
        """
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

    # def verify_swag_labs_inventory_page(self):
    #     self.bp_wait_for_page_to_load()
    #     try:
    #         assert self.bp_verify_url("https://www.saucedemo.com/inventory.html")
    #         assert self.bp_get_browser_title == "Swag Labs"
    #         assert self.bp_is_displayed(self.productsHeader, "Products Header")
    #         assert self.bp_is_enabled(self.productSortDropdown, "Products Sort")
    #         assert self.bp_get_all_items_from_dropdown_list(self.productSortDropdown,
    #                                                         "Product Sort Dropdown") == self.productSortDropdownValues
    #         assert self.bp_is_enabled(self.inventoryItemNames, "Inventory Item Names")
    #         assert self.bp_is_enabled(self.inventoryItemDescriptions, "Inventory Item Descriptions")
    #         assert self.bp_is_displayed(self.inventoryItemImages, "Inventory Item Images")
    #         assert self.bp_is_displayed(self.inventoryItemPrices, "Inventory Item Prices")
    #         assert self.bp_is_enabled(self.inventoryItemAddToCartButtons, "Inventory Item Add To Cart Buttons")
    #
    #         # verify filters working correctly
    #         self.bp_select_from_dropdown_list(self.productSortDropdown, "Name (A to Z)", "Product Sort Dropdown")
    #         assert self.bp_verify_column_sorting(self.inventory_item_names, "asc", "Inventory Item Names")
    #
    #         self.bp_select_from_dropdown_list(self.productSortDropdown, "Name (Z to A)", "Product Sort Dropdown")
    #         assert self.bp_verify_column_sorting(self.inventory_item_names, "desc", "Inventory Item Names")
    #
    #         self.bp_select_from_dropdown_list(self.productSortDropdown, "Price (low to high)", "Product Sort Dropdown")
    #         assert self.bp_verify_column_sorting(self.inventory_item_prices, "asc", "Inventory Item Prices")
    #
    #         self.bp_select_from_dropdown_list(self.productSortDropdown, "Price (high to low)", "Product Sort Dropdown")
    #         assert self.bp_verify_column_sorting(self.inventory_item_prices, "desc", "Inventory Item Prices")
    #     except AssertionError:
    #         print("Inventory Page not verified.")
    #         traceback.print_exc()
    #         return False
    #     print("Swag Labs Inventory Page Verified")
    #     return True
    #
    # def add_item_to_cart(self, item_name):
    #     actual_items = self.bp_get_all_items_from_dropdown_list(self.inventory_item_names)
    #     for index, item in enumerate(actual_items):
    #         if self.bp_get_text(item) == item_name:
    #             actual_add_to_cart_buttons = (self.bp_get_all_items_from_dropdown_list
    #                                           (self.inventory_item_add_to_cart_buttons))
    #             self.bp_click(actual_add_to_cart_buttons[index])
    #             return
    #     raise Exception("Item not found")

    # ========================================================================
    # PAGE VERIFICATION
    # ========================================================================

    def verify_page_url(self) -> bool:
        """Verify the current URL matches inventory page URL."""
        return self.bp_verify_url(self.EXPECTED_URL)

    def verify_page_title(self) -> bool:
        """Verify the page title is correct."""
        return self.bp_get_browser_title == self.EXPECTED_TITLE

    def verify_products_header_displayed(self) -> bool:
        """Verify products header is displayed."""
        return self.bp_is_displayed(self._products_header, "Products Header")

    def verify_sort_dropdown_enabled(self) -> bool:
        """Verify sort dropdown is enabled and contains correct options."""
        if not self.bp_is_enabled(self._product_sort_dropdown, "Product Sort Dropdown"):
            return False

        actual_options = self.bp_get_all_items_from_dropdown_list(
            self._product_sort_dropdown,
            "Product Sort Dropdown"
        )
        expected_options = list(self.SORT_OPTIONS.values())

        return actual_options == expected_options

    def verify_inventory_items_displayed(self) -> bool:
        """Verify all inventory item elements are displayed/enabled."""
        checks = [
            self.bp_is_enabled(self.inventoryItemNames, "Inventory Item Names"),
            self.bp_is_enabled(self.inventoryItemDescriptions, "Inventory Item Descriptions"),
            self.bp_is_displayed(self.inventoryItemImages, "Inventory Item Images"),
            self.bp_is_displayed(self.inventoryItemPrices, "Inventory Item Prices"),
            self.bp_is_enabled(self.inventoryItemAddToCartButtons, "Add To Cart Buttons")
        ]
        return all(checks)

    def verify_sort_functionality(self) -> bool:
        """
        Verify all sort options work correctly.

        Returns:
            bool: True if all sort options work, False otherwise
        """
        sort_tests = [
            (self.SORT_OPTIONS["name_asc"], self.inventory_item_names, "asc", "Item Names A-Z"),
            (self.SORT_OPTIONS["name_desc"], self.inventory_item_names, "desc", "Item Names Z-A"),
            (self.SORT_OPTIONS["price_asc"], self.inventory_item_prices, "asc", "Prices Low-High"),
            (self.SORT_OPTIONS["price_desc"], self.inventory_item_prices, "desc", "Prices High-Low")
        ]

        for sort_option, elements, order, description in sort_tests:
            self.bp_select_from_dropdown_list(
                self._product_sort_dropdown,
                sort_option,
                "Product Sort Dropdown"
            )

            if not self.bp_verify_column_sorting(elements, order, description):
                print(f"Sort verification failed for: {description}")
                return False

        return True

    def verify_swag_labs_inventory_page(self) -> bool:
        """
        Comprehensive verification of inventory page.

        Returns:
            bool: True if all verifications pass, False otherwise
        """
        self.bp_wait_for_page_to_load()

        verifications = {
            "URL": self.verify_page_url,
            "Page Title": self.verify_page_title,
            "Products Header": self.verify_products_header_displayed,
            "Sort Dropdown": self.verify_sort_dropdown_enabled,
            "Inventory Items": self.verify_inventory_items_displayed,
            "Sort Functionality": self.verify_sort_functionality
        }

        failed_checks = []

        for check_name, check_func in verifications.items():
            try:
                if not check_func():
                    failed_checks.append(check_name)
                    print(f"FAILED: {check_name} verification failed")
            except Exception as e:
                failed_checks.append(check_name)
                print(f"ERROR: {check_name} verification error: {str(e)}")

        if failed_checks:
            print(f"\nInventory Page verification failed. Failed checks: {', '.join(failed_checks)}")
            return False

        print("SUCCESS: Swag Labs Inventory Page Verified Successfully")
        return True

    # ========================================================================
    # CART OPERATIONS
    # ========================================================================

    def add_item_to_cart_by_name(self, item_name: str) -> bool:
        """
        Add an item to cart by its name.

        Args:
            item_name: Name of the item to add to cart

        Returns:
            bool: True if item was added, False otherwise

        Raises:
            ValueError: If item name is not found
        """
        item_elements = self.inventory_item_names

        for index, item_element in enumerate(item_elements):
            current_item_name = self.bp_get_text(item_element)

            if current_item_name == item_name:
                add_to_cart_buttons = self.inventory_item_add_to_cart_buttons

                if index < len(add_to_cart_buttons):
                    self.bp_click(add_to_cart_buttons[index])
                    print(f"SUCCESS: Added '{item_name}' to cart")
                    return True
                else:
                    print(f"ERROR: Add to cart button not found for '{item_name}'")
                    return False

        raise ValueError(f"Item '{item_name}' not found in inventory")

    def add_item_to_cart_by_index(self, index: int) -> bool:
        """
        Add an item to cart by its position index.

        Args:
            index: Zero-based index of the item

        Returns:
            bool: True if item was added, False otherwise
        """
        add_to_cart_buttons = self.inventory_item_add_to_cart_buttons

        if 0 <= index < len(add_to_cart_buttons):
            self.bp_click(add_to_cart_buttons[index])
            item_names = self.inventory_item_names
            item_name = self.bp_get_text(item_names[index]) if index < len(item_names) else "Unknown"
            print(f"SUCCESS: Added item at index {index} ('{item_name}') to cart")
            return True

        print(f"ERROR: Invalid index: {index}. Available items: {len(add_to_cart_buttons)}")
        return False

    def remove_item_from_cart_by_name(self, item_name: str) -> bool:
        """
        Remove an item from cart by its name.

        Args:
            item_name: Name of the item to remove

        Returns:
            bool: True if item was removed, False otherwise
        """
        item_elements = self.inventory_item_names

        for index, item_element in enumerate(item_elements):
            if self.bp_get_text(item_element) == item_name:
                remove_buttons = self.inventory_item_remove_from_cart_buttons

                if index < len(remove_buttons):
                    self.bp_click(remove_buttons[index])
                    print(f"SUCCESS: Removed '{item_name}' from cart")
                    return True

        print(f"ERROR: Item '{item_name}' not found in cart")
        return False

    def get_item_count(self) -> int:
        """
        Get total number of items displayed on inventory page.

        Returns:
            int: Number of inventory items
        """
        return len(self.inventory_item_names)

    def get_all_item_names(self) -> List[str]:
        """
        Get list of all item names on the page.

        Returns:
            List of item names as strings
        """
        item_elements = self.inventory_item_names
        return [self.bp_get_text(element) for element in item_elements]

    def get_all_item_prices(self) -> List[str]:
        """
        Get list of all item prices on the page.

        Returns:
            List of prices as strings
        """
        price_elements = self.inventory_item_prices
        return [self.bp_get_text(element) for element in price_elements]

    def is_item_in_cart(self, item_name: str) -> bool:
        """
        Check if an item is currently in the cart (has Remove button).

        Args:
            item_name: Name of the item to check

        Returns:
            bool: True if item is in cart, False otherwise
        """
        item_elements = self.inventory_item_names
        remove_buttons = self.inventory_item_remove_from_cart_buttons

        for index, item_element in enumerate(item_elements):
            if self.bp_get_text(item_element) == item_name:
                return index < len(remove_buttons)

        return False
