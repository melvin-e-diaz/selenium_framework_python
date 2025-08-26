import os

import pytest

# from src.main.python.com.selenium.framework.base.BrowserSetup import BrowserSetup
from selenium_framework_python.src.main.python.com.selenium.framework.base.BrowserSetup import BrowserSetup

driver = None


# must name file conftest.py so that it is run for setup and teardown
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="edge",
        help="Selects the web browser to execute tests on: Firefox, Chrome, Edge. Default browser is Edge."
    )
    parser.addoption(
        "--headless",
        action="store",
        default=False,
        help='Enter True to run the browser in headless mode.'
    )


@pytest.fixture()
def setup(request):
    global driver

    browser_setup = BrowserSetup(driver)
    driver = browser_setup.initialize_browser(request.config.getoption("--browser_name"),
                                              request.config.getoption("--headless"))

    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver  # Before test function execution
    driver.close()  # post your test function execution


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     """
#         Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
#         :param item:
#         """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
#             file_name = os.path.join(reports_dir, report.nodeid.replace("::", "_") + ".png")
#             print("file name is " + file_name)
#             # _capture_screenshot( file_name )
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extras = extra

# def _capture_screenshot(file_name):
# driver.get_screenshot_as_file(file_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['selenium_driver']
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# make a screenshot with a name of the test, date and time
def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/", "_").replace("::", "__")
    driver.save_screenshot(file_name)

