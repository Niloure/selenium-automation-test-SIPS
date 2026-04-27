import pytest
import os
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

load_dotenv()

def get_credential(role: str):
    """Return (username, password) for given role."""
    username = os.getenv(f"{role.upper()}_USERNAME")
    password = os.getenv(f"{role.upper()}_PASSWORD")
    if not username or not password:
        raise ValueError(f"Missing credentials for role {role} in .env file")
    return username, password

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("BASE_URL", "http://localhost:3000"),
        help="base url for application"
    )
    
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="browser to run tests on"
    )
    
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="run browser in headless mode"
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture
def headless(request):
    return request.config.getoption("--headless")


@pytest.fixture
def driver(request, browser, headless):
    driver = _create_driver(browser, headless)
    
    yield driver
    
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        _save_screenshot(driver, request.node.name)
    
    driver.quit()


def _create_driver(browser: str, headless: bool):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        _configure_chrome_options(options, headless)
        return webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        _configure_firefox_options(options, headless)
        return webdriver.Firefox(options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        _configure_edge_options(options, headless)
        return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")


def _configure_chrome_options(options, headless: bool):
    # Pastikan folder download mengarah ke folder yang bisa dipantau (opsional)
    # Jika tidak diset, dia akan masuk ke folder Downloads default sistem.
    
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # INI KUNCI UNTUK MASALAH ADOBE ACROBAT:
        "plugins.always_open_pdf_externally": True,  # Download PDF, jangan dibuka
        "pdfjs.disabled": True,                       # Matikan viewer internal Chrome
        "download.prompt_for_download": False,        # Jangan tanya mau simpan di mana
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True                  # Hindari dialog konfirmasi keamanan download
    })
    
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    if headless:
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")


def _configure_firefox_options(options, headless: bool):
    options.set_preference("signon.autofillForms", False)
    options.set_preference("signon.rememberSignons", False)
    options.add_argument("--start-maximized")
    
    if headless:
        options.add_argument("--headless")


def _configure_edge_options(options, headless: bool):
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    
    if headless:
        options.add_argument("--headless")


def _save_screenshot(driver, test_name: str):
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    file_path = os.path.join(screenshot_dir, f"FAILED_{test_name}_{timestamp}.png")
    
    driver.save_screenshot(file_path)
    print(f"\nScreenshot saved: {file_path}")


@pytest.fixture
def login_as(driver, base_url):
    def _login(username: str, password: str):
        login_page = LoginPage(driver, base_url)
        login_page.open()
        login_page.login(username, password)
        dashboard = DashboardPage(driver, base_url)
        dashboard.wait_until_loaded()
        return dashboard
    return _login


@pytest.fixture
def master_admin_creds():
    return get_credential("master_admin")

@pytest.fixture
def admin_creds():
    return get_credential("admin")

@pytest.fixture
def kepala_badan_creds():
    return get_credential("kepala_badan")

@pytest.fixture
def sekretaris_creds():
    return get_credential("sekretaris")

@pytest.fixture(params=["master_admin", "admin", "kepala_badan", "sekretaris"])
def all_role_creds(request):
    return get_credential(request.param)


@pytest.fixture
def authenticated_dashboard(login_as, request):
    username = getattr(request, "param", {}).get("username", "admin")
    password = getattr(request, "param", {}).get("password", "admin")
    return login_as(username, password)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_configure(config):
    config.addinivalue_line("markers", "auth: tests for authentication")
    config.addinivalue_line("markers", "positive: tests for positive scenarios")
    config.addinivalue_line("markers", "negative: tests for negative scenarios")
    config.addinivalue_line("markers", "protection: tests for authentication and authorization")
    config.addinivalue_line("markers", "role_based: tests for role-based access control")
    config.addinivalue_line("markers", "visibility: tests for menu visibility based on roles")
    config.addinivalue_line("markers", "admin: tests for admin role")
    config.addinivalue_line("markers", "master_admin: tests for master admin role")
    config.addinivalue_line("markers", "kepala_badan: tests for kepala badan role")
    config.addinivalue_line("markers", "sekretaris_badan: tests for sekretaris badan role")
    config.addinivalue_line("markers", "klasifikasi: tests for klasifikasi surat feature")
    config.addinivalue_line("markers", "surat_masuk: tests for surat masuk feature")
    config.addinivalue_line("markers", "surat_keluar: tests for surat keluar feature")
    config.addinivalue_line("markers", "cetak_agenda: tests for cetak agenda feature")
    config.addinivalue_line("markers", "disposisi: tests for disposisi feature")
    config.addinivalue_line("markers", "manage_user: tests for manage user feature")


def pytest_sessionstart(session):
    print(f"\nTest session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {session.config.getoption('--base-url')}")
    print(f"Browser: {session.config.getoption('--browser')}")
    print(f"Headless: {session.config.getoption('--headless')}")


def pytest_sessionfinish(session, exitstatus):
    print(f"\nTest session finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Exit status: {exitstatus}")