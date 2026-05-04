import os

import allure
import pytest
from playwright.sync_api import Page

from core.settings import settings
from pages.login_page import LoginPage
from pages.create_booking_page import CreateBookingPage
from services.auth_service import AuthService
from services.booking_service import BookingService
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def booking_page(page: Page):
    return CreateBookingPage(page)


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def booking_service():
    return BookingService()


@pytest.fixture(scope="session")
def authenticated_auth_service():
    """Fixture that logs in once per session and returns an authenticated AuthService."""
    service = AuthService()
    payload = service.get_login_payload()
    response = service.login(payload)
    assert response.status_code == 200, f"Session login failed: {response.text}"
    logger.info("Session-level authentication successful")
    yield service
    service.clear_token()


# --- Allure screenshot hook for UI failures ---

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Attach screenshot on UI test failure
    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture is not None:
            try:
                screenshot = page_fixture.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"{item.name}_failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                logger.warning(f"Could not attach screenshot: {exc}")

        # Attach API request/response log if auth_service was used
        auth_fixture = item.funcargs.get("auth_service")
        if auth_fixture is not None:
            try:
                log_path = os.path.join(settings.LOG_DIR, "api_requests.log")
                if os.path.exists(log_path):
                    with open(log_path, "r") as f:
                        log_content = f.read()[-5000:]  # Last 5KB
                    allure.attach(
                        log_content,
                        name="api_request_log",
                        attachment_type=allure.attachment_type.TEXT,
                    )
            except Exception as exc:
                logger.warning(f"Could not attach API log: {exc}")
