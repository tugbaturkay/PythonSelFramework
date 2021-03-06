import pytest
from selenium import webdriver
import time
driver = None

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name=request.config.getoption("browser_name")
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument("headless")
        chrome_options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe", options=chrome_options)
        driver.delete_all_cookies()
        driver.maximize_window()

        '''
        Below code is put to show that crossbrowser testing can be done
        but tests have not been ran against FF. 
        '''
    # elif browser_name == "firefox":
    #     driver = webdriver.Firefox(executable_path="C:\\geckodriver.exe")
    #     driver.maximize_window()

    driver.implicitly_wait(5)
    driver.get("http://automationpractice.com/index.php")
    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        file_name = "./screenshots/" + report.nodeid.replace("::", "_") + ".png"
        _capture_screenshot(file_name)
        if file_name:
            html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
            extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)

def pytest_configure(config):
    config.option.htmlpath = './report.html'




