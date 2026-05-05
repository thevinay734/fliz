import pytest
from playwright.sync_api import Page, expect

from factories.vendor_factory import VendorFactory
from pages.login_page import LoginPage
from pages.vendor_signup_page import VendorSignupPage


@pytest.fixture
def vendor_signup_page(page: Page):
    return VendorSignupPage(page)


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.mark.ui
def test_vendor_signup_full_flow(login_page: LoginPage, vendor_signup_page: VendorSignupPage):
    # Generate dummy vendor data
    vendor = VendorFactory.create()

    # 1. Open website
    login_page.goto("https://dev.fliz.com.sa/ar/renter/companies")

    # 2. Switch to English and wait for navigation
    login_page.page.locator("img").nth(3).click()
    login_page.page.get_by_text("English").click()
    login_page.page.wait_for_url("**/en/**", timeout=15000)
    login_page.page.wait_for_load_state("networkidle")

    # 3. Vendor signup flow with dummy data
    vendor_signup_page.signup_as_vendor(
        company_name=vendor["company_name"],
        email=vendor["email"],
        address_query=vendor["address_query"],
        address_option=vendor["address_option"],
        phone=vendor["phone"],
        message=vendor["message"],
        password=vendor["password"],
        document_path="/Users/vinaymac/Vinay_automation_projects/Fliz/test_files/dummy_vendor_image.png",
    )

    # 4. Verify: should leave the register page after submission
    page = login_page.page
    page.wait_for_timeout(5000)
    expect(page).not_to_have_url("register", timeout=15000)
