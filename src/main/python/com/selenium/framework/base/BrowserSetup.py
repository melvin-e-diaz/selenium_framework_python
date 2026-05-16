# import platform
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
#
# from selenium_framework_python.src.main.python.com.selenium.framework.base.BasePage import BasePage
#
#
# class BrowserSetup(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.driver = driver
#
#     def initialize_browser(self, browser_type="edge", headless=False):
#         match browser_type.lower():
#             case "chrome":
#                 self.driver = self.chrome_setup(headless)
#             case "edge":
#                 self.driver = self.edge_setup(headless)
#             case "firefox":
#                 self.driver = self.firefox_setup(headless)
#             case "safari":
#                 self.driver = self.safari_setup(headless)
#             case _:
#                 raise Exception("Invalid browser type.")
#
#         return self.driver
#
#     @staticmethod
#     def chrome_setup(headless=False):
#         chrome_options = webdriver.ChromeOptions()
#         chrome_service = BrowserSetup.set_webdriver_path("chrome")
#         chrome_options.add_argument("--disable-extensions")
#         chrome_options.add_argument("--remote-allow-origins=*")
#         if headless:
#             chrome_options.add_argument("--headless")
#         return webdriver.Chrome(options=chrome_options, service=chrome_service)
#
#     @staticmethod
#     def edge_setup(headless=False):
#         edge_options = webdriver.EdgeOptions()
#         edge_options.use_chromium = True
#         edge_service = BrowserSetup.set_webdriver_path("edge")
#         if headless:
#             edge_options.add_argument("--headless")
#         return webdriver.Edge(options=edge_options, service=edge_service)
#
#     @staticmethod
#     def firefox_setup(headless=False):
#         firefox_options = webdriver.FirefoxOptions()
#         firefox_service = BrowserSetup.set_webdriver_path("firefox")
#         if headless:
#             firefox_options.add_argument("--headless")
#         return webdriver.Firefox(options=firefox_options, service=firefox_service)
#
#     @staticmethod
#     def safari_setup(headless=False):
#         safari_options = webdriver.SafariOptions()
#         if headless:
#             safari_options.add_argument("--headless")
#         safari_service = webdriver.SafariService(enable_logging=True)
#         return webdriver.Safari(service=safari_service, options=safari_options)
#
#     @staticmethod
#     def set_webdriver_path(browser):
#         browser_service = None
#         var1 = browser
#         var2 = None
#         beginning_path = "C:/Users/bb31/PycharmProjects/selenium_automation_python/selenium_framework_python"  # change this to your local path
#         match browser:
#             case "chrome":
#                 var2 = browser
#             case "edge":
#                 var2 = "msedge"
#             case "firefox":
#                 var2 = "gecko"
#         match platform.system():
#             case "Windows":
#                 browser_service = Service(f"{beginning_path}/libs/{var1}/windows/{var2}driver.exe")
#             case "Linux":
#                 browser_service = Service(f"{beginning_path}/libs/{var1}/linux/{var2}driver")
#             case "Darwin":
#                 browser_service = Service(f"{beginning_path}/libs/{var1}/mac/{var2}driver")
#         return browser_service

import platform
import os
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService

from selenium_framework_python.src.main.python.com.selenium.framework.base.BasePage import BasePage


class BrowserSetup(BasePage):
    """Handles browser initialization and configuration for Selenium WebDriver."""

    # Driver name mappings for path construction
    DRIVER_NAMES = {
        "chrome": "chromedriver",
        "edge": "msedgedriver",
        "firefox": "geckodriver"
    }

    # Platform-specific directory names
    PLATFORM_DIRS = {
        "Windows": "windows",
        "Linux": "linux",
        "Darwin": "mac"
    }

    def __init__(self, driver: Optional[webdriver.Remote] = None):
        """
        Initialize BrowserSetup.

        Args:
            driver: Optional existing WebDriver instance
        """
        super().__init__(driver)
        if driver is not None:
            self.driver = driver

    def initialize_browser(self, browser_type: str = "edge", headless: bool = False) -> webdriver.Remote:
        """
        Initialize and return a WebDriver instance.

        Args:
            browser_type: Browser to use ("chrome", "edge", "firefox", "safari")
            headless: Whether to run browser in headless mode

        Returns:
            Configured WebDriver instance

        Raises:
            ValueError: If browser_type is invalid
        """
        browser_methods = {
            "chrome": self.chrome_setup,
            "edge": self.edge_setup,
            "firefox": self.firefox_setup,
            "safari": self.safari_setup
        }

        browser_key = browser_type.lower()
        if browser_key not in browser_methods:
            raise ValueError(
                f"Invalid browser type: {browser_type}. "
                f"Valid options: {', '.join(browser_methods.keys())}"
            )

        self.driver = browser_methods[browser_key](headless)
        return self.driver

    @staticmethod
    def chrome_setup(headless: bool = False) -> webdriver.Chrome:
        """Configure and return Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-allow-origins=*")

        if headless:
            options.add_argument("--headless=new")  # Use new headless mode

        service = BrowserSetup._get_webdriver_service("chrome", ChromeService)
        return webdriver.Chrome(options=options, service=service)

    @staticmethod
    def edge_setup(headless: bool = False) -> webdriver.Edge:
        """Configure and return Edge WebDriver."""
        options = webdriver.EdgeOptions()

        if headless:
            options.add_argument("--headless=new")  # Use new headless mode

        service = BrowserSetup._get_webdriver_service("edge", EdgeService)
        return webdriver.Edge(options=options, service=service)

    @staticmethod
    def firefox_setup(headless: bool = False) -> webdriver.Firefox:
        """Configure and return Firefox WebDriver."""
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        service = BrowserSetup._get_webdriver_service("firefox", FirefoxService)
        return webdriver.Firefox(options=options, service=service)

    @staticmethod
    def safari_setup(headless: bool = False) -> webdriver.Safari:
        """
        Configure and return Safari WebDriver.

        Note: Safari does not support headless mode. The headless parameter
        is accepted for API consistency but will be ignored.
        """
        if headless:
            print("Warning: Safari does not support headless mode. Ignoring headless parameter.")

        service = SafariService(enable_logging=True)
        return webdriver.Safari(service=service)

    @staticmethod
    def _get_webdriver_service(browser: str, service_class):
        """
        Get platform-specific WebDriver service.

        Args:
            browser: Browser name ("chrome", "edge", "firefox")
            service_class: Service class to instantiate

        Returns:
            Configured Service instance

        Raises:
            RuntimeError: If platform is unsupported or driver not found
        """
        # Get project root dynamically
        current_file = Path(__file__)
        project_root = current_file.parent
        while project_root.name != "selenium_framework_python" and project_root.parent != project_root:
            project_root = project_root.parent

        # Determine platform
        system = platform.system()
        platform_dir = BrowserSetup.PLATFORM_DIRS.get(system)

        if not platform_dir:
            raise RuntimeError(f"Unsupported platform: {system}")

        # Get driver name
        driver_name = BrowserSetup.DRIVER_NAMES.get(browser)
        if not driver_name:
            raise ValueError(f"Unknown browser: {browser}")

        # Construct driver path
        extension = ".exe" if system == "Windows" else ""
        driver_path = project_root / "libs" / browser / platform_dir / f"{driver_name}{extension}"

        # Validate driver exists
        if not driver_path.exists():
            raise FileNotFoundError(
                f"WebDriver not found at: {driver_path}\n"
                f"Please ensure the driver is installed in the correct location."
            )

        return service_class(str(driver_path))