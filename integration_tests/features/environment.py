from os import getenv

from behave import use_fixture
from behave_webdriver.fixtures import fixture_browser
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager


def before_all(context):
    setup_webdriver(context)


def setup_webdriver(context):
    driver_args = download_webdriver()

    # Pass webdriver-path to setup-call
    use_fixture(fixture_browser, context, **driver_args)


def download_webdriver(default_driver=None):
    browser_env = getenv('BEHAVE_WEBDRIVER', default_driver)
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
        path = EdgeChromiumDriverManager().install()
    elif browser_env == 'opera':
        path = OperaDriverManager().install()
    elif browser_env == 'safari':
        pass  # Only runs on macOS with preinstalled Safari
    else:
        raise ValueError("Invalid driver '{}' found in env-variable 'BEHAVE_WEBDRIVER'".format(browser_env))
    return {
        **({"executable_path": path} if path is not None else {}),
        **({"options": options} if options is not None else {})
    }
