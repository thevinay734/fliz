import re
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from config.config import BASE_URL


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


def test_login_page_loads(login_page: LoginPage):
    login_page.navigate()


def test_login_with_valid_credentials(page: Page, login_page: LoginPage):
    from data.test_data import LOGIN_PAYLOAD
    login_page.login(LOGIN_PAYLOAD["phoneNumber"], LOGIN_PAYLOAD["password"])
    expect(page).to_have_url(re.compile(".*(home|dashboard|user).*"))


def test_login_invalid_credentials(login_page: LoginPage):
    login_page.login("0000000000", "wrongpassword")
    login_page.expect_error_visible()
