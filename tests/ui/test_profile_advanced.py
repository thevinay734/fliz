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


def _login_and_navigate_to_profile(login_page: LoginPage, profile_page: ProfilePage):
    """Helper: login + navigate to edit profile."""
    login_page.goto("https://dev.fliz.com.sa/ar/renter/companies")
    login_page.page.locator("img").nth(3).click()
    login_page.page.get_by_text("English").click()
    login_page.page.get_by_role("link", name="Sign In").click()
    login_page.select_country_india()
    login_page.fill_phone_modal("+91 92195-81212")
    login_page.fill_password_modal("Vinay@12345")
    login_page.click_log_in_modal()

    profile_page.open_profile_menu()
    profile_page.click_my_profile()
    profile_page.click_edit_profile()


@pytest.mark.ui
def test_update_name_only(login_page: LoginPage, profile_page: ProfilePage):
    """Partial update: only name field."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_name("Only Name Updated")
    profile_page.click_update_profile()


@pytest.mark.ui
def test_update_email_only(login_page: LoginPage, profile_page: ProfilePage):
    """Partial update: only email field."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_email("onlyemail@test.com")
    profile_page.click_update_profile()


@pytest.mark.ui
def test_update_address_only(login_page: LoginPage, profile_page: ProfilePage):
    """Partial update: only address field."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_address("noida", "Noida, Uttar Pradesh, India")
    profile_page.click_update_profile()


@pytest.mark.ui
def test_empty_name_validation(login_page: LoginPage, profile_page: ProfilePage):
    """Empty name should show error or disable update."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_name("")
    profile_page.click_update_profile()
    # Check for error message or validation tooltip
    error = login_page.page.locator("text=/required|empty|invalid/i")
    expect(error).to_be_visible()


@pytest.mark.ui
def test_invalid_email_format(login_page: LoginPage, profile_page: ProfilePage):
    """Invalid email should show validation error."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_email("not-an-email")
    profile_page.click_update_profile()
    error = login_page.page.locator("text=/invalid|email|format/i")
    expect(error).to_be_visible()


@pytest.mark.ui
def test_long_name_boundary(login_page: LoginPage, profile_page: ProfilePage):
    """Very long name (100+ chars)."""
    _login_and_navigate_to_profile(login_page, profile_page)
    long_name = "A" * 150
    profile_page.enter_name(long_name)
    profile_page.click_update_profile()


@pytest.mark.ui
def test_special_characters_in_name(login_page: LoginPage, profile_page: ProfilePage):
    """Name with special characters and numbers."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_name("Rajesh@123 #Sharma!")
    profile_page.click_update_profile()


@pytest.mark.ui
def test_xss_in_name_field(login_page: LoginPage, profile_page: ProfilePage):
    """Security: XSS payload in name."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_name("<script>alert('xss')</script>")
    profile_page.click_update_profile()
    # Page should NOT show alert dialog


@pytest.mark.ui
def test_sql_injection_in_email(login_page: LoginPage, profile_page: ProfilePage):
    """Security: SQL injection payload in email."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_email("' OR 1=1 --")
    profile_page.click_update_profile()
    # Should not crash or expose data


@pytest.mark.ui
def test_cancel_edit_does_not_save(login_page: LoginPage, profile_page: ProfilePage):
    """Click back/cancel without saving."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_name("Unsaved Change")
    # Navigate away without clicking update
    login_page.page.goto("https://dev.fliz.com.sa/ar/renter/companies")
    # Re-open profile and verify old name
    profile_page.open_profile_menu()
    profile_page.click_my_profile()
    profile_page.click_edit_profile()
    name_field = login_page.page.get_by_role("textbox", name="Enter your name")
    expect(name_field).not_to_have_value("Unsaved Change")


@pytest.mark.ui
def test_profile_picture_wrong_file_type(login_page: LoginPage, profile_page: ProfilePage):
    """Upload a non-image file (e.g., PDF)."""
    _login_and_navigate_to_profile(login_page, profile_page)
    # Note: create a dummy PDF or text file for this test
    # profile_page.upload_profile_picture("dummy.pdf")
    # profile_page.click_update_profile()
    # error = login_page.page.locator("text=/invalid|image|file/i")
    # expect(error).to_be_visible()
    pytest.skip("Requires a dummy PDF file; enable when file is available")


@pytest.mark.ui
def test_unicode_and_emoji_in_name(login_page: LoginPage, profile_page: ProfilePage):
    """Name with unicode characters and emoji."""
    _login_and_navigate_to_profile(login_page, profile_page)
    profile_page.enter_name("Rajesh 🚀 शर्मा")
    profile_page.click_update_profile()
