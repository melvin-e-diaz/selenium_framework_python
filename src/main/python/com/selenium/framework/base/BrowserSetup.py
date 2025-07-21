import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.main.python.com.selenium.framework.base.BasePage import BasePage


class BrowserSetup(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def initialize_browser(self, browser_type="edge", headless=False):
        match browser_type.lower():
            case "chrome":
                self.driver = self.chrome_setup(headless)
            case "edge":
                self.driver = self.edge_setup(headless)
            case "firefox":
                self.driver = self.firefox_setup(headless)
            case "safari":
                self.driver = self.safari_setup(headless)
            case _:
                raise Exception("Invalid browser type.")

        return self.driver

    @staticmethod
    def chrome_setup(headless=False):
        chrome_options = webdriver.ChromeOptions()
        chrome_service = BrowserSetup.set_webdriver_path("chrome")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--remote-allow-origins=*")
        if headless:
            chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options, service=chrome_service)

    @staticmethod
    def edge_setup(headless=False):
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True
        edge_service = BrowserSetup.set_webdriver_path("edge")
        if headless:
            edge_options.add_argument("--headless")
        return webdriver.Edge(options=edge_options, service=edge_service)

    @staticmethod
    def firefox_setup(headless=False):
        firefox_options = webdriver.FirefoxOptions()
        firefox_service = BrowserSetup.set_webdriver_path("firefox")
        if headless:
            firefox_options.add_argument("--headless")
        return webdriver.Firefox(options=firefox_options, service=firefox_service)

    @staticmethod
    def safari_setup(headless=False):
        safari_options = webdriver.SafariOptions()
        if headless:
            safari_options.add_argument("--headless")
        safari_service = webdriver.SafariService(enable_logging=True)
        return webdriver.Safari(service=safari_service, options=safari_options)

    @staticmethod
    def set_webdriver_path(browser):
        browser_service = None
        var1 = browser
        var2 = None
        beginningPath = "C:/Users/melvi/PycharmProjects/SeleniumFramework_Python"  # change this to your local path
        match browser:
            case "chrome":
                var2 = browser
            case "edge":
                var2 = "msedge"
            case "firefox":
                var2 = "gecko"
        match platform.system():
            case "Windows":
                browser_service = Service(f"{beginningPath}/libs/{var1}/windows/{var2}driver.exe")
            case "Linux":
                browser_service = Service(f"{beginningPath}/libs/{var1}/linux/{var2}driver")
            case "Darwin":
                browser_service = Service(f"{beginningPath}/libs/{var1}/mac/{var2}driver")
        return browser_service
