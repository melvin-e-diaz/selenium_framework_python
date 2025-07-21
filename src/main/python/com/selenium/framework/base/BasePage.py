import datetime
import random
import string
import time
import traceback
from datetime import date
from datetime import datetime

from selenium.webdriver import ActionChains
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
bp_click(element, description = None)
    Overrides the PageFactory click function. Function first checks if the element is clickable
    and highlights the element before clicking the button. If a description is included, the
    function will print a log of the web driver action to the console.
bp_right_click(element, description = None)
    Overrides the PageFactory right click function. Function first checks if the element is clickable
    and highlights the element before performing a right_click. If a description is included, the
    function will print a log of the web driver action to the console.
bp_double_click(element, description = None)
    Overrides the PageFactory double click function. Function first checks if the element is clickable
    and highlights the element before performing a double_click. If a description is included, the
    function will print a log of the web driver action to the console.
bp_click_and_hold(element, description = None)
    Overrides the PageFactory click_and_hold function. Function first checks if the element is clickable
    and highlights the element before performing a click_and_hold. If a description is included, the
    function will print a log of the web driver action to the console.
bp_release_click(element, description = None)
    Overrides the PageFactory release_click function. Function highlights the element before performing a
    release_click. If a description is included, the function will print a log of the web driver action
    to the console.
bp_mouse_hover(element, description = None)
    Overrides the PageFactory mouse_hover function. Function highlights the element before performing a
    mouse_hover. If a description is included, the function will print a log of the web driver action to
    the console.
bp_mouse_hover_with_offset(self, element, x, y, description = None)
    Overrides the PageFactory mouse_hover function. Function highlights the element before performing a
    mouse_hover to the coordinates x and y. If a description is included, the function will print a log
    of the web driver action to the console.
bp_write_text(element, text, description = None)
    Overrides the PageFactory set_text function. Function first checks if the element is visible, then
    highlights the element, clears the element, and then writes the text given in the text parameter. If
    a description is included, the function will print a log of the web action to the console.
bp_get_text(element, text, description = None)
    Overrides the PageFactory get_text() function. Function first checks for the visibility of the element,
    then returns the text found in the web element. If a description is included, the function will print a log
    of the web driver action and the text returned to the console.
bp_is_checked(element, description = None)
    Overrides the PageFactory is_checked() function. This function must be run on a checkbox or a radio button.
    Function first checks for visibility of the element, then returns whether the element is checked. If a description
    is included, the function will print a log of the web driver action and if the element is checked or not to the
    console.
bp_is_displayed(element, description = None)
    Overrides the PageFactory is_displayed() function. This function first checks if the element is visible,
    then returns a    boolean representing if the element is displayed. If a description is included, the function will
     print a log of the web driver action and if the element is displayed or not to the console.
bp_is_enabled(element, description = None)
    Overrides the PageFactory is_enabled() function. This function first checks if the element is visible and then
    returns a    boolean representing if the element is enabled. If a description is included, the function will print
    a log of the web    driver action and if the element is enabled or not to the console.
bp_select_from_dropdown_list(element, text, description = None)
    Overrides the PageFactory select_element_by_text and select_element_by_value functions. Element must have a [select]
    html tag. This function first checks if the element is visible. If the text entered is a String, it will call the
    PageFactory select_element_by_text function. Otherwise, it will call the PageFactory select_element_by_value
    function. If a description is entered, the function will print a log of the web driver action and what value was
    selected from the dropdown list.
bp_select_from_dropdown_list_using_index(element, index, description = None)
    Overrides the PageFactory select_element_by_index function. The function first checks if the element is visible.
    It will then call the PageFactory select_element_by_index function. If a description is entered, the function will
    print a log of the web driver action and what index was selected from the dropdown list.
bp_get_num_items_from_dropdown_list(element, description = None)
    Overrides the PageFactory get_list_item_count function. The function first checks if the element is visible. It will
    then call the PageFactory get_list_item_count function and return an int representing the number of items in the
    list. If a description is entered, the function will print a log of the web driver action and the number of items
    found in the dropdown list.
bp_get_all_items_from_dropdown_list(element, description = None)
    Overrides the PageFactory get_all_list_item function. The function first checks if the element is visible. It will
    then call the PageFactory get_all_list_item function and return an List[WebElement] representing all of the items
    in the list. If a description is entered, the function will print a log of the web driver action.
bp_deselect_all_items_from_dropdown_list(element, description = None)
    Overrides the PageFactory deselect_all function. The function first checks if the element is visible. It will then
    call the PageFactory deselect_all function. If a description is entered, the function will print a log of the web
    driver action.
bp_move_to_element(element, description = None)
    Function to move to a given element on the page using Javascript. If a description is entered, the function will
    print a log of the web driver action to the console.
bp_scroll_down()
    Function to scroll down the page by (0, 3000). Function will print a log of the scroll down action to the console.
bp_scroll_by_amount(x, y)
    Function to scroll down the page by (x, y). Function will print a log of the scroll down action to the console.
bp_scroll_to_bottom_of_page()
    Function to scroll down to the bottom of the web page. Function will print a log of the scroll down action to the
    console.
bp_scroll_to_top_of_page()
    Function to scroll to the top of the web page. Function will print a log of the scroll function to the console.
bp_enter_random_text(element, text_length = 15, description = None)
    Function to enter a randomly generated String. Length of string set to text_length (default = 15 characters). If a
    description is included, a log of the action will be printed to the console along with the randomly generated word.
bp_return_todays_date()
    Static method to return the current date and time.
bp_handle_alert(accept_or_dismiss = True)
    Function to handle a web page popup alert. If the accept_or_dismiss parameter = True, function will accept the
    alert, otherwise, it will dismiss the alert (default is True). Log of action will be written to the console.
bp_switch_to_new_window(num_windows_open = 0)
    Function to switch to a new web browser tab. Function will first wait for the expected number of windows to be
    num_windows_open + 1 (num_windows_open defaults to 0). It will then switch to num_windows_open+1 and print a log to
    the console.
bp_close_popup_window(num_windows_to_be_open = 1)
    Function to close a popup window. num_windows_to_be_open can be used if there are more than 2 windows open. This
    parameter will throw an exception if the value entered is less than 1
bp_browser_back()
    Function to hit the BACK button on the web browser.
bp_browser_forward()
    Function to hit the FORWARD button on the web browser.
bp_browser_refresh()
    Function to refresh the web browser.
bp_browser_close()
    Function to close the web browser
bp_verify_column_sorting(column, asc_or_desc = "asc", description = None)
    Function to verify the sorting of a column of type List[WebElement]. Function will make a copy of the list, and
    perform a sort either ascending or descending based on the asc_or_desc parameter (defaults to asc), and then compare
    the lists. If the lists are equal, the function returns True, otherwise it returns False and will print both lists
    to the console.
bp_switch_to_frame(iframe)
    Switches the browser to the frame given by the iframe parameter. Web element must have the [iframe] HTML tag.
bp_switch_to_default_content()
    Switches the browser to the default content.
bp_get_browser_title()
    Returns a String value of the title found in the browser. Also prints the title to the console.
bp_wait_for_page_to_load()
    Function to wait until the web page is completely loaded. Function will print to the console the time needed to load
    the web page.
bp_print_timestamp()
    Function to print the current timestamp.
generate_random_string(string_length)
    Function to generate a random string of specified length using letters and digits
bp_verify_url(expected_url)
    Function to verify the current URL of the driver against the expected URL
bp_handle_error(e, error_text)
    Function to standardize error reporting, with e being the exception and error_text describing the error. Function
    will also print the stack trace.
"""

    def __init__(self, driver):
        super().__init__()
        self.element = None
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.highlight = True
        self.mobile_test = False

    def bp_click(self, element, description=None):
        self.element = element
        self.element.element_to_be_clickable()
        self.highlight_web_element(element)
        self.element.click_button()
        if description:
            print(f"{self.bp_print_timestamp()} | Clicked on element: {description}")

    def bp_right_click(self, element, description=None):
        self.element = element
        self.element.element_to_be_clickable()
        self.highlight_web_element(element)
        self.element.context_click()
        if description:
            print(f"{self.bp_print_timestamp()} | Right clicked on element: {description}")

    def bp_double_click(self, element, description=None):
        self.element = element
        self.element.element_to_be_clickable()
        self.highlight_web_element(element)
        self.element.double_click()
        if description:
            print(f"{self.bp_print_timestamp()} | Double clicked on element:{description}")

    def bp_click_and_hold(self, element, description=None):
        self.element = element
        self.element.element_to_be_clickable()
        self.highlight_web_element(element)
        self.element.click_and_hold()
        if description:
            print(f"{self.bp_print_timestamp()} | Click and hold on element:{description}")

    def bp_release_click(self, element, description=None):
        self.element = element
        self.element.release()
        if description:
            print(f"{self.bp_print_timestamp()} | Released click on element:{description}")

    def bp_mouse_hover(self, element, description=None):
        self.element = element
        self.element.hover()
        if description:
            print(f"{self.bp_print_timestamp()} | Mouse hover on element:{description}")

    def bp_mouse_hover_with_offset(self, element, x, y, description=None):
        self.element = element
        self.element.hover_with_offset(x, y)
        if description:
            print(f"{self.bp_print_timestamp()} | Mouse hover on element:{description} with offset: {x},{y}")

    def bp_write_text(self, element, text, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        self.highlight_web_element(element)
        self.element.clear_text()
        self.element.set_text(text)
        if description:
            print(f"{self.bp_print_timestamp()} | Write text {text} on element: {description}")

    def bp_get_text(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if self.element.get_text and description:
            print(f"{self.bp_print_timestamp()} | Returned text {self.element.get_text()} from element: {description}")
        elif self.element.get_text is None and description:
            print(f"{self.bp_print_timestamp()} | ERROR returning text from element: {description}")
        return self.element.get_text()

    def bp_is_checked(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if self.element.is_Checked() and description:
            print(f"{self.bp_print_timestamp()} | Element checked is TRUE: {description}")
        elif self.element.is_Checked() is False and description:
            print(f"{self.bp_print_timestamp()} | Element checked is FALSE: {description}")
        return self.element.is_Checked()

    def bp_is_displayed(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if description:
            if self.element.is_displayed():
                print(f"{self.bp_print_timestamp()} | Element displayed is TRUE: {description}")
            else:
                print(f"{self.bp_print_timestamp()} | ERROR: Element is NOT displayed: {description}")
        return self.element.is_displayed()

    def bp_is_enabled(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if description:
            if self.element.is_enabled():
                print(f"{self.bp_print_timestamp()} | Element enabled is TRUE: {description}")
            else:
                print(f"{self.bp_print_timestamp()} | Element enabled is FALSE: {description}")
        return self.element.is_enabled()

    def bp_select_from_dropdown_list(self, element, text, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if isinstance(text, str):
            self.element.select_element_by_text(text)
            if description:
                print(f"{self.bp_print_timestamp()} | Selected option {text} from element: {description}")
        else:
            self.element.select_element_by_value(text)
            if description:
                print(f"{self.bp_print_timestamp()} | Selected value {text} from element: {description}")

    def bp_select_from_dropdown_list_using_index(self, element, index, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        self.element.select_element_by_index(index)
        if description:
            print(f"{self.bp_print_timestamp()} | Selected option with index: {index} from element: {description}")

    def bp_get_num_items_from_dropdown_list(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if description:
            print(
                f"{self.bp_print_timestamp()} | Number of items in {description} dropdown list:"
                f" {self.element.get_num_of_items()}")
        return self.element.get_list_item_count()

    def bp_get_all_items_from_dropdown_list(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if description:
            print(f"{self.bp_print_timestamp()} | All items in {description} dropdown list:")
        for item in self.element.get_all_list_item():
            print(item)
        return self.element.get_all_list_item()

    def bp_get_selected_items_from_dropdown_list(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if description:
            print(f"{self.bp_print_timestamp()} | All selected items in {description} dropdown list:")
        for item in self.element.get_list_selected_item():
            print(item)
        return self.element.get_list_selected_item()

    def bp_verify_item_contained_in_dropdown_list(self, element, item, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        if description:
            if self.element.verify_list_item(item):
                print(f"{self.bp_print_timestamp()} | TRUE: Item {item} found in {description} dropdown list:")
            else:
                print(f"{self.bp_print_timestamp()} | FALSE: Item {item} NOT found in {description} dropdown list:")
        return self.element.verify_list_item(item)

    def bp_deselect_all_items_from_dropdown_list(self, element, description=None):
        self.element = element
        self.element.visibility_of_element_located()
        select = Select(element)
        select.deselect_all()
        if description:
            print(f"{self.bp_print_timestamp()} | All items deselected from {description} dropdown list:")

    def bp_move_to_element(self, element, description=None):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        if description:
            print(f"{self.bp_print_timestamp()} | Moved to element {description}")

    def bp_scroll_down(self):
        actions = ActionChains(self.driver)
        actions.scroll_by_amount(0, 3000).perform()
        print(f"{self.bp_print_timestamp()} | Scroll down")

    def bp_scroll_by_amount(self, x, y):
        actions = ActionChains(self.driver)
        actions.scroll_by_amount(x, y).perform()
        print(f"Scroll down by amount: {x} x {y}")

    def bp_scroll_to_bottom_of_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"{self.bp_print_timestamp()} | Scroll to bottom of page")

    def bp_scroll_to_top_of_page(self):
        self.driver.execute_script("window.scrollTo(0, 0;")
        print(f"{self.bp_print_timestamp()} | Scroll to top of page")

    def bp_enter_random_text(self, element, text_length=15, description=None):
        self.element = element
        self.element.element_to_be_clickable()
        self.highlight_web_element(element)
        random_text = self.generate_random_string(text_length)
        self.bp_write_text(element, random_text)
        if description:
            print(f"{self.bp_print_timestamp()} | Entered random text: {random_text} into element: {description}")

    @staticmethod
    def bp_return_todays_date():
        return date.today()

    def bp_handle_alert(self, accept_or_dismiss="accept"):
        self.wait.until(expected_conditions.alert_is_present())
        print(f"{self.bp_print_timestamp()} | Alert detected.")
        alert = self.driver.switch_to.alert
        print(alert.text)
        if accept_or_dismiss == "accept":
            alert.accept()
            print(f"{self.bp_print_timestamp()} | Alert accepted.")
        else:
            alert.dismiss()
            print(f"{self.bp_print_timestamp()} | Alert dismissed.")

    def bp_switch_to_new_window(self, num_windows_open=0):
        self.wait.until(expected_conditions.number_of_windows_to_be(num_windows_open + 2))
        windows_opened = self.driver.window_handles
        self.driver.switch_to.window(windows_opened[num_windows_open + 1])
        print(f"{self.bp_print_timestamp()} | Switch to new window: {num_windows_open + 1}")

    def bp_close_popup_window(self, num_windows_to_be_open=1):
        if num_windows_to_be_open < 1:
            raise Exception("num_windows_to_be_open must be 1 or greater")
        windows_opened = self.driver.window_handles
        self.bp_browser_close()
        self.driver.switch_to.window(windows_opened[num_windows_to_be_open - 1])
        print(f"{self.bp_print_timestamp()} | Closed popup window")

    def bp_browser_back(self):
        self.driver.back()
        print(f"{self.bp_print_timestamp()} | Browser back")

    def bp_browser_forward(self):
        self.driver.forward()
        print(f"{self.bp_print_timestamp()} | Browser forward")

    def bp_browser_refresh(self):
        self.driver.refresh()
        print(f"{self.bp_print_timestamp()} | Browser refresh")

    def bp_browser_close(self):
        self.driver.close()
        print(f"{self.bp_print_timestamp()} | Browser close")

    def bp_verify_column_sorting(self, column, asc_or_desc="asc", description=None):
        sorted_list = []
        for counter in column:
            sorted_list.append(counter.get_text())
        original_list = sorted_list.copy()
        if asc_or_desc == "asc":
            sorted_list.sort()
        else:
            sorted_list.sort(reverse=True)
        if sorted_list == original_list:
            if description:
                print(
                    f"{self.bp_print_timestamp()} | TRUE: Sorting column {description} by {asc_or_desc} order"
                    f" verified.")
            return True
        else:
            if description:
                print(
                    f"{self.bp_print_timestamp()} | FALSE: Sorting column {description} by {asc_or_desc} order NOT"
                    f" verified.")
            else:
                print(f"{self.bp_print_timestamp()} | FALSE: Sorting column by {asc_or_desc} order NOT verified.")
            print("Original list:")
            for item in original_list:
                print(item)
            print("Sorted list:")
            for item in sorted_list:
                print(item)
            return False

    def bp_switch_to_frame(self, iframe):
        self.wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(iframe))
        self.driver.switch_to.frame(iframe)
        print(f"{self.bp_print_timestamp()} | Switch to frame: {iframe}")

    def bp_switch_to_default_content(self):
        self.driver.switch_to.default_content()
        print(f"{self.bp_print_timestamp()} | Switch to default content")

    @property
    def bp_get_browser_title(self):
        print(f"{self.bp_print_timestamp()} | Browser title: {self.driver.title}")
        return self.driver.title

    def bp_wait_for_page_to_load(self):
        print(f"{self.bp_print_timestamp()} | Waiting for page to load")
        start_time = time.perf_counter()
        self.wait.until(lambda driver: driver.execute_script("return document.readyState;") == "complete")
        end_time = time.perf_counter()
        print(f"{self.bp_print_timestamp} | Time elapsed for page load: {end_time - start_time}")

    @staticmethod
    def bp_print_timestamp():
        current_timestamp = datetime.now()
        return current_timestamp

    @staticmethod
    def generate_random_string(string_length):
        """Generates a random string of specified length using letters and digits."""
        characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase letters, and digits
        random_string = ''.join(random.choice(characters) for i in range(string_length))
        return random_string

    def bp_verify_url(self, expected_url):
        actual_url = self.driver.current_url
        if actual_url == expected_url:
            print(f"{self.bp_print_timestamp()} | URL verified: {expected_url}")
            return True
        else:
            print(f"{self.bp_print_timestamp()} | URL not verified: Expected: {expected_url} | Actual: {actual_url}")
            return False

    def bp_handle_error(self, e, error_text):
        print(f"{self.bp_print_timestamp()} | ERROR: | {error_text}")
        traceback.print_exc()
