import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


@pytest.fixture
def profile_page(page: Page):
    return ProfilePage(page)


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.mark.ui
def test_update_profile_full_flow(login_page: LoginPage, profile_page: ProfilePage):
    # 1. Open website
    login_page.goto("https://dev.fliz.com.sa/ar/renter/companies")

    # 2. Switch to English
    login_page.page.locator("img").nth(3).click()
    login_page.page.get_by_text("English").click()

    # 3. Click Sign In
    login_page.page.get_by_role("link", name="Sign In").click()

    # 4. Select India
    login_page.select_country_india()

    # 5. Enter phone + password
    login_page.fill_phone_modal("+91 92195-81212")
    login_page.fill_password_modal("Vinay@12345")
    login_page.click_log_in_modal()

    # 6. Update profile
    profile_page.update_profile(
        name="Rajesh Sharma",
        email="rajesh@gmail.com",
        address_query="tecorb",
        address_option="Tecorb Technologies, B Block",
    )
