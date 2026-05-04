import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.config import BASE_URL


def test_login_page_loads(login_page: LoginPage):
    login_page.navigate()


def test_login_with_valid_credentials(page: Page, login_page: LoginPage):
    from data.test_data import LOGIN_PAYLOAD
    login_page.login(LOGIN_PAYLOAD["phoneNumber"], LOGIN_PAYLOAD["password"])
    expect(page).to_have_url(re.compile(".*(home|dashboard|user).*"))


def test_login_invalid_credentials(page: Page):
    page.goto(f"{BASE_URL}login")
    page.get_by_placeholder("Phone number").fill("0000000000")
    page.get_by_placeholder("Password").fill("wrongpassword")
    page.get_by_role("button", name=re.compile("Login|Sign In", re.IGNORECASE)).click()

    error_message = page.locator("text=/invalid|incorrect|wrong|error/i")
    expect(error_message).to_be_visible()
