from os import getenv
from sys import platform
from urllib.parse import urljoin

from behave import use_fixture
from behave_webdriver.driver import BehaveDriverMixin
from behave_webdriver.fixtures import fixture_browser
from msedge.selenium_tools import Edge, EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager


def before_all(context):
    context.base_url = "http://localhost"
    setup_webdriver(context)
    # Warmup backend by calling endpoint that accesses database
    context.behave_driver.get(urljoin(context.base_url, "/database/monster"))


def setup_webdriver(context):
    driver_args = download_webdriver()

    # Pass webdriver-path to setup-call
    use_fixture(fixture_browser, context, **driver_args)


def download_webdriver(default_driver=None):
    browser_env = getenv('BEHAVE_WEBDRIVER', default_driver)
    webdriver = None
    path = None
    options = None
    if browser_env == 'chrome':
        path = ChromeDriverManager().install()
        options = ChromeOptions()
        options.headless = True
    elif browser_env == 'firefox':
        path = GeckoDriverManager().install()
        options = FirefoxOptions()
        options.headless = True
    # Flandria is not supporting Internet Explorer
    # elif browser_env == 'ie':
    #    path = IEDriverManager().install()
    elif browser_env == 'edge':
        webdriver = EdgeDriver  # Swap out selenium.webdriver.Edge with msedge.selenium_tools.Edge to use EdgeOptions
        path = EdgeChromiumDriverManager().install()
        options = EdgeOptions()
        options.use_chromium = True
        options.headless = True
        if platform.startswith('linux'):
            options.set_capability('platform', 'LINUX')
    elif browser_env == 'opera':
        path = OperaDriverManager().install()
    elif browser_env == 'safari':
        pass  # Only runs on macOS with preinstalled Safari
    else:
        raise ValueError("Invalid driver '{}' found in env-variable 'BEHAVE_WEBDRIVER'".format(browser_env))
    return {
        **({"webdriver": webdriver} if webdriver is not None else {}),
        **({"executable_path": path} if path is not None else {}),
        **({"options": options} if options is not None else {})
    }


class EdgeDriver(BehaveDriverMixin, Edge):
    pass
