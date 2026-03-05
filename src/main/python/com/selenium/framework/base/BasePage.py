import datetime
import random
import string
import time
import traceback
from datetime import date
from datetime import datetime
from typing import Optional, List

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory import PageFactory


class BasePage(PageFactory):
    """
A class that contains the core functions for the Selenium automated testing framework.
This class sits on top of the PageFactory class and inherits all of its methods.

...

Attributes:
----------
element: WebElement
    represents the Selenium web element to be interacted with
driver: WebDriver
    represents the Selenium web driver that performs the interactions with the web elements
wait: WebDriverWait
    time in seconds that the web driver will wait before failing a test (default is 10)
highlight: Boolean
    highlights the element that the web driver is currently interacting with (default is True)
mobile_test: Boolean
    determines if testing is run for mobile tests (default is False, feature not yet implemented)

Methods
-------
See individual method docstrings for detailed information.
"""

    # ============================================================================
    # CONSTRUCTOR
    # ============================================================================
    def __init__(self, driver, wait_timeout=10, highlight=True, mobile_test=False):
        """
        Initialize the Selenium BasePage.

        Parameters
        ----------
        driver: Selenium WebDriver instance
        wait_timeout: Maximum time to wait for elements (default: 10 sec)
        highlight: Whether to highlight elements during interactions (default: True)
        mobile_test: Whether test is executed on mobile browser (not yet implemented; default: False)
        """
        super().__init__()
        self.element = None
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait_timeout)
        self.highlight = highlight
        self.mobile_test = mobile_test

    # ============================================================================
    # LOGGING FUNCTION
    # ============================================================================
    def _log(self, message, description: Optional[str] = None) -> None:
        """
        Internal method designed to consistently log actions.

        Parameters
        ----------
        message: The action message to log.
        description: Element description. Default: None
        """
        timestamp = self.bp_print_timestamp()
        if description:
            print(f"{timestamp} | {message}: {description}")
        else:
            print(f"{timestamp}) | {message}")

    # ============================================================================
    # CLICK FUNCTIONS
    # ============================================================================
    def bp_click(self, element, description: Optional[str] = None, click_type="left") -> None:
        """
        Function to handle clicking on a web element.

        Parameters
        ----------
        element: element to click
        description: Description for logging purposes. Default=None
        click_type: The type of click to be performed (left, right, double). Default=left
        """
        try:
            element.element_to_be_clickable()
            self.highlight_web_element(element)
            match click_type.lower():
                case "left":
                    element.click_button()
                case "right":
                    element.context_click()
                case "double":
                    element.double_click()
                case _:
                    raise Exception(f"Invalid click_type entered: {click_type}")
            self._log(f"{click_type} clicked on element", description)
        except Exception as e:
            self.bp_handle_error(f"Failed to {click_type} click {description or 'element'}: {e}")
            raise

    def bp_click_and_hold(self, element, description: Optional[str] = None) -> None:
        """
        Function to click and hold on a web element.

        Parameters
        ----------
        element: The element to be clicked on.
        description: Optional description. Default=None
        """
        try:
            element.element_to_be_clickable()
            self.highlight_web_element(element)
            element.click_and_hold()
            self._log("Click and hold on element", description)
        except Exception as e:
            self.bp_handle_error(f"Failed to click and hold {description or 'element'}: {e}")
            raise

    def bp_release_click(self, element, description: Optional[str] = None) -> None:
        """
        Function to release a click that was previously held. Use in conjunction with the bp_click_and_hold() function.

        Parameters
        ----------
        element: The element to be clicked on.
        description: Optional description. Default=None
        """
        try:
            element.release()
            self._log("Released click on element", description)
        except Exception as e:
            self.bp_handle_error(f"Failed to click and hold {description or 'element'}: {e}")
            raise

    def bp_mouse_hover(self, element, description: Optional[str] = None, x: Optional[int | float] = None,
                       y: Optional[int | float] = None, ) -> None:
        """
        Function to hover the mouse over a specific element with an optional offset.

        Parameters
        ----------
        element: Web element to be hovered over.
        description: Optional description for logging purposes. Default=None
        x: X-axis offset. Default=None
        y: Y-axis offset. Default=None
        """
        try:
            self.highlight_web_element(element)
            if x and y:
                element.hover_with_offset(x, y)
            elif x or y:
                self._log("WARNING: One offset coordinate is missing. Please check the code. Running hover method with "
                          "no offset.")
                element.hover()
            else:
                element.hover()
            message = f"Mouse hover on element with offset ({x},{y})" if x and y else "Mouse hover on element"
            self._log(message, description)
        except Exception as e:
            error_msg = f"Failed to hover over {description or 'element'} with offset ({x},{y})" if x and y else \
                f"Failed to hover over {description or 'element'} "
            self.bp_handle_error(f"{error_msg}: {e}")

    # ============================================================================
    # WRITE TEXT FUNCTION
    # ============================================================================
    def bp_write_text(self, element, text, description: Optional[str] = None, clear_text: Optional[bool] = True) \
            -> None:
        """
        Function to write text to a web element.

        Parameters
        ----------
        element: WebElement to write text to.
        text: Text to be written to element.
        description: Optional description for logging purposes. Default=None
        clear_text: Flag that determines whether the text field should be cleared of any text before writing the text.
            Default=True
        """
        try:
            element.visibility_of_element_located()
            self.highlight_web_element(element)
            if clear_text:
                element.clear_text()
            element.set_text(text)
            desc = description or "unknown element"
            self._log(f"Wrote {text} to element {desc}")
        except Exception as e:
            self.bp_handle_error(f"Failed to write text to {description or 'unknown element'}: {e}")
            raise

    # ============================================================================
    # GET TEXT FUNCTION
    # ============================================================================
    def bp_get_text(self, element, description: Optional[str] = None) -> str:
        """
        Function to return visible text contained in a web element.
        Parameters
        ----------
        element: The web element to be analyzed.
        description: Optional description of the web element for debugging purposes

        Returns
        -------
        str of text contained in visible element.
        """
        try:
            element.visibility_of_element_located()
            text = element.get_text()
            if text:
                self._log(f"Returned text '{text}' from element.", description or 'unknown element')
            else:
                self._log(f"WARNING: No text found in element.", description or 'unknown element')
            return text
        except Exception as e:
            self.bp_handle_error(f"Failed to get text from {description or 'unknown element'}: {e}")
            raise

    # ============================================================================
    # VERIFICATION METHODS
    # ============================================================================
    def bp_is_checked(self, element, description: Optional[str] = None) -> bool:
        """
        Function to check if a checkbox element is checked.
        Parameters
        ----------
        element: Web Element representing the checkbox
        description: Optional description for logging purposes. Default=None

        Returns
        -------
        Boolean representing if the value is checked or not. Returns True if the value is checked, False if the value is
        not checked.
        """
        try:
            element.visibility_of_element_located()
            is_checked = element.is_Checked()
            self._log(f"Element checked status is {is_checked}", description or "unknown element")
            return is_checked
        except Exception as e:
            self.bp_handle_error(f"Attempting to verify check/no check status failed for "
                                 f"{description or 'unknown element'}: {e}")

    def bp_is_displayed(self, element, description: Optional[str] = None) -> bool:
        """
        Function to check if a web element is displayed.
        Parameters
        ----------
        element: Web Element to be checked.
        description: Optional description. Default = none

        Returns
        -------
        True if the web element is displayed on the page, False if the web element is not displayed on the page
        """
        try:
            element.visibility_of_element_located()
            is_displayed = element.is_displayed()
            self._log(f"Element displayed is {is_displayed}", description or "unknown element")
            return is_displayed
        except Exception as e:
            self.bp_handle_error(f"Attempting to verify displayed status failed for "
                                 f"{description or 'unknown element'}: {e}")
            raise

    def bp_is_enabled(self, element, description: Optional[str] = None) -> bool:
        """
        Function to verify if the web element is enabled on the page.

        Parameters
        ----------
        element: Web Element to be checked.
        description: Optional description. Default=None

        Returns
        -------
        True if the element is enabled on the page, False otherwise.
        """
        try:
            element.visibility_of_element_located()
            is_enabled = element.is_enabled()
            self._log(f"Element enabled is {is_enabled}", description or "unknown element")
            return is_enabled
        except Exception as e:
            self.bp_handle_error(f"Attempting to verify enabled status failed for "
                                 f"{description or 'unknown element'}: {e}")
            raise

    # ============================================================================
    # DROPDOWN LIST METHODS
    # ============================================================================
    def bp_select_from_dropdown_list(self, element, text_or_value, description: Optional[str] = None,
                                     select_by_index: Optional[bool] = False) -> None:
        """
        Function to select from a dropdown list. List defaults to selecting from a dropdown list by the value or text.
        To select by the index, set select_by_index = True
        Parameters
        ----------
        element: Web element to select.
        text_or_value: Value to be selected from the dropdown list.
        description: Optional description for logging purposes. Default=None
        select_by_index: Optional bool to select by index instead of value. Default=False (select by value). Set to True
            to select by index.
        """
        try:
            element.visibility_of_element_located()
            if select_by_index:
                element.select_element_by_index(text_or_value)
                self._log(f"Selected index {text_or_value} from element", description or 'unknown element')
                return
            elif isinstance(text_or_value, str):
                element.select_element_by_text(text_or_value)
            else:
                element.select_element_by_value(text_or_value)
            self._log(f"Selected option {text_or_value} from element", description or 'unknown element')
        except Exception as e:
            self.bp_handle_error(f"Failed to select option {text_or_value} from dropdown list "
                                 f"{description or 'unknown element'}: {e}")

    def bp_get_num_items_from_dropdown_list(self, element, description: Optional[str] = None) -> int:
        """
        Function to return the number of items present in a dropdown list.

        Parameters
        ----------
        element: Web Element to be analyzed.
        description: Optional description for logging purposes.

        Returns
        -------
        num_items: int value representing the number of items
        """
        try:
            element.visibility_of_element_located()
            num_items = element.get_list_item_count()
            self._log(f"Found {num_items} items in dropdown list.", description or "unknown element")
            return num_items
        except Exception as e:
            self.bp_handle_error(f"Failed to return number of items in dropdown list {description or 'element'}: {e}")
            raise

    def bp_get_items_from_dropdown_list(self, element, description: Optional[str] = None,
                                        selected_items: Optional[bool] = False) -> List[WebElement]:
        """
        Function to return items from a dropdown list. Use selected_items = True to return items that are selected from
            a multi-select list instead of all items.

        Parameters
        ----------
        element: WebElement target element
        description: Optional description for logging. Default=None
        selected_items: bool flag to return selected items instead of all items.

        Returns
        -------
        List[WebElement] representing the elements returned from the dropdown list.
        """
        try:
            element.visibility_of_element_located()
            if selected_items:
                items = element.get_list_selected_item()
            else:
                items = element.get_all_list_item()
            if len(items) == 0:
                self._log("WARNING: No items found in dropdown list", description or 'unknown list')
            else:
                self._log(f"{'Selected' if selected_items else 'All'} items found in dropdown list: ",
                          description or 'unknown list')
                for item in items:
                    print(f"    - {item}")
            return items
        except Exception as e:
            self.bp_handle_error(f"Failed to get items from {description or 'element'}: {e}")
            raise

    def bp_verify_item_present_in_dropdown_list(self, element, item, description: Optional[str] = None) -> bool:
        """
        Function to verify if an item is present in a dropdown list.

        Parameters
        ----------
        element: WebElement representing the target element.
        item: item to verify if it is in dropdown list
        description: Optional description for logging purposes. Default=None

        Returns
        -------
        is_found: bool True if item is found in dropdown list, False if not found.
        """
        try:
            element.visibility_of_element_located()
            is_present = element.verify_list_item(item)

            self._log(f"{is_present}: Item {item} is {'present' if is_present else 'not present'} in dropdown list",
                      description or 'unknown element')
            return is_present
        except Exception as e:
            self.bp_handle_error(f"Failed to verify presence of item {item} in dropdown list "
                                 f"{description or 'unknown element'}: {e}")
            raise

    def bp_deselect_all_items_from_dropdown_list(self, element, description: Optional[str] = None) -> None:
        """
        Function to deselect all items from a dropdown list.

        Parameters
        ----------
        element: WebElement representing the target element.
        description: Optional description for logging purposes. Default=None
        """
        try:
            element.visibility_of_element_located()
            select = Select(element)
            select.deselect_all()
            self._log("All items deselected from dropdown list.", description or 'unknown element')
        except Exception as e:
            self.bp_handle_error(f"Failed to deselect all items from {description or 'unknown element'}: {e}")
            raise

    # ============================================================================
    # MOVE AND SCROLL METHODS
    # ============================================================================
    def bp_move_to_element(self, element, description: Optional[str] = None) -> None:
        """
        Function to move the screen to the target element.

        Parameters
        ----------
        element: WebElement representing the target element.
        description: Optional description for logging purposes. Default=None
        """
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self._log("Moved to element", description or 'unknown element')
        except Exception as e:
            self.bp_handle_error(f"Failed to move to {description or 'unknown element'}: {e}")
            raise

    def bp_scroll(self, direction: Optional[str] = None, amount: Optional[int] = None, x: Optional[int] = None,
                  y: Optional[int] = None, element=None) -> None:
        """
        Unified scroll function that handles all scroll operations.

        Parameters:
            direction: String specifying scroll direction - "up", "down", "left", "right",
                      "top", "bottom". Mutually exclusive with x/y coordinates.
            amount: Pixels to scroll when using direction (default: 3000 for up/down, 1000 for left/right)
            x: Specific x-coordinate to scroll to (use with y for absolute positioning)
            y: Specific y-coordinate to scroll to (use with x for absolute positioning)
            element: WebElement to scroll to (brings element into view)

        Examples:
            bp_scroll(direction="down")  # Scroll down 3000px
            bp_scroll(direction="up", amount=500)  # Scroll up 500px
            bp_scroll(direction="top")  # Scroll to top of page
            bp_scroll(direction="bottom")  # Scroll to bottom of page
            bp_scroll(x=0, y=1000)  # Scroll to coordinates (0, 1000)
            bp_scroll(element=some_element)  # Scroll element into view
        """
        try:
            # Scroll to element
            if element is not None:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           element)
                self._log_simple(f"Scrolled to element: {element}")
                return

            # Scroll to specific coordinates
            if x is not None or y is not None:
                scroll_x = x if x is not None else 0
                scroll_y = y if y is not None else 0
                self.driver.execute_script(f"window.scrollTo({scroll_x}, {scroll_y});")
                timestamp = self.bp_print_timestamp()
                print(f"{timestamp} | Scrolled to coordinates: x={scroll_x}, y={scroll_y}")
                return

            # Scroll by direction
            if direction is None:
                raise ValueError("Must specify either direction, coordinates (x, y), or element")

            direction = direction.lower()

            # Handle top/bottom special cases
            if direction == "top":
                self.driver.execute_script("window.scrollTo(0, 0);")
                self._log_simple("Scrolled to top of page")
                return

            if direction == "bottom":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self._log_simple("Scrolled to bottom of page")
                return

            # Handle directional scrolling with ActionChains
            scroll_map = {
                "down": (0, amount or 3000),
                "up": (0, -(amount or 3000)),
                "right": (amount or 1000, 0),
                "left": (-(amount or 1000), 0)
            }

            if direction not in scroll_map:
                raise ValueError(f"Invalid direction: {direction}. Must be one of: up, down, left, right, top, bottom")

            scroll_x, scroll_y = scroll_map[direction]
            actions = ActionChains(self.driver)
            actions.scroll_by_amount(scroll_x, scroll_y).perform()

            timestamp = self.bp_print_timestamp()
            print(f"{timestamp} | Scrolled {direction} by x={scroll_x}, y={scroll_y}")

        except ValueError as ve:
            # Re-raise ValueError with original message
            raise ve
        except Exception as e:
            self.bp_handle_error(f"Failed to scroll: {e}")
            raise

    # def bp_enter_random_text(self, element, text_length: Optional[int] = 15, description: Optional[str] = None):
    #     """
    #     Function to enter randomly generated text into a web element
    #
    #     Parameters
    #     ----------
    #     element: WebElement representing the target element
    #     text_length: Optional parameter to set the length of random text. Default=15
    #     description: Optional text for logging purposes. Default=None
    #     """
    #     self.element = element
    #     self.element.element_to_be_clickable()
    #     self.highlight_web_element(element)
    #     random_text = self.bp_generate_random_string(text_length)
    #     self.bp_write_text(element, random_text)
    #     if description:
    #         print(f"{self.bp_print_timestamp()} | Entered random text: {random_text} into element: {description}")

    @staticmethod
    def bp_return_todays_date() -> date:
        """
        Function to return today's date.
        Returns
        -------
        date: Today's date
        """
        return date.today()

    def bp_handle_alert(self, dismiss: Optional[bool] = False) -> None:
        """
        Function to handle a popup alert. Set dismiss=False to dismiss the alert, otherwise the alert will be accepted.

        Parameters
        ----------
        dismiss: Optional bool. Set this to True for the alert to be dismissed, otherwise it will be accepted.
        """
        try:
            self.wait.until(expected_conditions.alert_is_present())
            self._log("Alert detected.")

            alert = self.driver.switch_to.alert
            self._log("Alert text:", alert.text)

            if dismiss:
                alert.dismiss()
                self._log("Alert dismissed.")
            else:
                alert.accept()
                self._log("Alert accepted.")
        except Exception as e:
            self.bp_handle_error(f"Failed to handle alert: {e}")
            raise

    def bp_switch_to_new_window(self, num_windows_open: Optional[int] = 0) -> None:
        """
        Function to switch driver to a new window.

        Parameters
        ----------
        num_windows_open: Int value representing the number of windows that are open. Default is 0
        """
        try:
            self.wait.until(expected_conditions.number_of_windows_to_be(num_windows_open + 2))
            windows_opened = self.driver.window_handles
            self.driver.switch_to.window(windows_opened[num_windows_open + 1])
            self._log(f"Switched to new window: {num_windows_open + 1}")
        except Exception as e:
            self.bp_handle_error(f"Failed to switch to new window: {e}")
            raise

    def bp_close_popup_window(self, num_windows_to_be_open: Optional[int] = 1) -> None:
        """
        Function to close a popup window

        Parameters
        ----------
        num_windows_to_be_open: int representing the number of windows expected to be open after the function has been
        completed. Default=1
        """
        if num_windows_to_be_open < 1:
            raise ValueError("ERROR: num_windows_to_be_open argument must be 1 or greater.")

        try:
            windows_opened = self.driver.window_handles
            self.bp_browser_close()
            self.driver.switch_to.window(windows_opened[num_windows_to_be_open - 1])
            self._log("Closed popup window.")
        except Exception as e:
            self.bp_handle_error(f"Failed to close popup window: {e}")
            raise

    def bp_browser_back(self) -> None:
        """
        Function to select Back in the web browser.
        """
        try:
            self.driver.back()
            self._log("Browser back.")
        except Exception as e:
            self.bp_handle_error(f"Failed to navigate back in the browser: {e}")
            raise

    def bp_browser_forward(self) -> None:
        """
        Function to navigate forward in the web browser.
        """
        try:
            self.driver.forward()
            self._log("Browser forward.")
        except Exception as e:
            self.bp_handle_error(f"Failed to navigate forward in the browser: {e}")

    def bp_browser_refresh(self) -> None:
        """
        Function to refresh the browser window.
        """
        try:
            self.driver.refresh()
            self._log("Browser refresh.")
        except Exception as e:
            self.bp_handle_error(f"Failed to refresh the browser: {e}")

    def bp_browser_close(self) -> None:
        """
        Function to close the browser window.
        """
        try:
            self.driver.close()
            print(f"{self.bp_print_timestamp()} | Browser close")
        except Exception as e:
            self.bp_handle_error(f"Failed to close the browser window: {e}")

    def bp_verify_column_sorting(self, column, description: Optional[str] = None, reverse_sort: Optional[bool] = False,
                                 sort_type: Optional[str] = 'string', date_format: Optional[str] = "%Y-%m-%d") -> bool:
        """
        Function to verify the sorting of a column in the UI versus sorting using Python's built-in sorting function.

        Parameters
        ----------
        column: WebElement representing the column to be verified.
        description: Optional description for logging purposes: Default=None
        reverse_sort: Optional, bool to sort in descending order. Default=False (ascending order)
        sort_type: Optional, str Determines method to sort function. Valid options are 'string', 'numeric', 'date'.
            Default=string
        date_format: Optional, str determines date format for sorting dates. Value must be a valid date format that can
            be processed by the Python datetime library. Default="%Y-%m-%d"

        Returns
        -------
        True if column sorting verified. False if column sorting is not verified.
        """

        # extract text from web elements and strip whitespace
        original_list = [counter.get_text().strip() for counter in column]
        sorted_list = original_list.copy()

        try:
            # sort based on type
            if sort_type == "numeric":
                sorted_list.sort(
                    key=lambda x: float(x) if x and x.replace('.', '', 1).replace('-', '', 1).isdigit() else float(
                        'inf'),
                    reverse=reverse_sort)
            elif sort_type == "date":
                sorted_list.sort(
                    key=lambda x: datetime.strptime(x, date_format) if x else datetime.min, reverse=reverse_sort)
            else:  # string
                sorted_list.sort(key=lambda x: x.lower() if x else "", reverse=reverse_sort)
        except (ValueError, TypeError) as e:
            self.bp_handle_error(f"Failed to sort column: {description or 'unknown column'} | {e}")
            return False

        # list comparison
        is_sorted = (sorted_list == original_list)
        asc_or_desc = 'descending' if reverse_sort else 'ascending'

        if is_sorted:
            self._log(f"TRUE: Column sorting verified in {asc_or_desc} order | Sort type: {sort_type}",
                      description or 'unknown column')
        else:
            self._log(f"FALSE: Column sorting not verified in {asc_or_desc} order | Sort type: {sort_type}",
                      description or 'unknown column')

            # print data for debugging purposes
            print("=====ORIGINAL LIST=====")
            for i, item in enumerate(original_list, 1):
                print(f"    {i} | {item}")

            print("=====EXPECTED SORTED LIST=====")
            for i, item in enumerate(sorted_list, 1):
                print(f"    {i} | {item}")

            return False

    def bp_switch_to_frame(self, iframe) -> None:
        """
        Function to switch to a specific iframe. Web element must have the iframe HTML tag.
        Parameters
        ----------
        iframe: WebElement representing the iframe to switch to.
        """
        try:
            self.wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(iframe))
            self.driver.switch_to.frame(iframe)
            self._log(f"Switched to frame {iframe}")
        except Exception as e:
            self.bp_handle_error(f"Failed to switch to iframe: {e}")
            raise

    def bp_switch_to_default_content(self) -> None:
        """
        Function to switch to default content.
        """
        try:
            self.driver.switch_to.default_content()
            self._log("Switch to default content.")
        except Exception as e:
            self.bp_handle_error(f"Failed to switch to default content: {e}")
            raise

    @property
    def bp_get_browser_title(self) -> str:
        """
        Function to retrieve the browser title
        Returns
        -------
        title: str representing the browser title
        """
        try:
            title = self.driver.title
            self._log(f"Browser title = {title}")
            return title
        except Exception as e:
            self.bp_handle_error(f"Failed to get browser title: {e}")
            raise

    def bp_wait_for_page_to_load(self) -> None:
        """
        Function to wait for the page to fully load. Elapsed time printed to log.
        """
        try:
            self._log("Waiting for page to load.")
            start_time = time.perf_counter()
            self.wait.until(lambda driver: driver.execute_script("return document.readyState;") == "complete")
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            self._log(f"Time elapsed for page load: {elapsed_time:.2f} seconds.")
        except Exception as e:
            self.bp_handle_error(f"Failed while waiting for page load: {e}")

    @staticmethod
    def bp_print_timestamp() -> datetime:
        """
        Returns the current timestamp
        Returns
        -------
        datetime: Current timestamp.
        """
        return datetime.now()

    @staticmethod
    def bp_generate_random_string(string_length: int) -> str:
        """
        Generates a random string of specified length using letters and digits.
        Parameters
        ----------
        string_length: int length of the string to generate

        Returns
        -------
        str: random string containing letters and digits.
        """
        characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase letters, and digits
        random_string = ''.join(random.choice(characters) for _ in range(string_length))
        return random_string

    def bp_verify_url(self, expected_url: str) -> bool:
        """
        Function to verify the URL
        Parameters
        ----------
        expected_url: String representing the expected URL

        Returns
        -------
        True if the actual URL and the expected URL match, False if they do not match.
        """
        try:
            actual_url = self.driver.current_url
            is_match = actual_url == expected_url
            if is_match:
                self._log(f"URL verified: {expected_url}")
            else:
                self._log(f"URL NOT verified. Expected URL: {expected_url} | Actual URL: {actual_url}")
            return is_match
        except Exception as e:
            self.bp_handle_error(f"Failed to verify URL: {e}")
            raise

    def bp_handle_error(self, error_text: str) -> None:
        """
        Function to handle and log errors with the stack trace.

        Parameters
        ----------
        error_text: Description of the error.
        """
        timestamp = self.bp_print_timestamp()
        print(f"{timestamp} | ERROR: {error_text}")
        traceback.print_exc()
