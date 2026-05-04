import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.login_page import LoginPage


PASSWORD = "Vinay@12345"


@pytest.fixture
def home_page(page: Page):
    return HomePage(page)


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.mark.ui
def test_login_full_flow(home_page: HomePage, login_page: LoginPage):
    # 1. Open website and switch to English
    home_page.navigate()
    home_page.click_language_toggle()
    home_page.select_english()

    # 2. Open sign-in modal
    home_page.click_sign_in()

    # 3. Log in via modal
    login_page.login_via_modal("+91 97943-05933", PASSWORD)

    # 4. Verify successful login
    login_page.expect_not_on_login_page()
