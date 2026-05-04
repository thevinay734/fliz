import re
import pytest
from playwright.sync_api import Page, expect
from config.config import BASE_URL


PASSWORD = "Vinay@12345"


@pytest.mark.ui
def test_login_full_flow(page: Page):
    # 1. Open website
    page.goto(BASE_URL)

    # 2. Click language toggle image
    page.locator("img").nth(3).click()

    # 3. Select English
    page.get_by_text("English").click()

    # 4. Click Sign In (سجل in English)
    page.get_by_role("link", name="Sign In").click()

    # 5. Open country code selector
    page.get_by_role("button", name="Saudi Arabia: +").click()

    # 6. Search for India
    page.get_by_role("searchbox", name="Search country").fill("ind")

    # 7. Select India (+91)
    page.get_by_text("+91").click()

    # 8. Enter phone number
    page.get_by_role("textbox", name="Member Phone Number").fill("+91 97943-05933")

    # 9. Enter password
    page.get_by_role("textbox", name="Enter Your Password").fill(PASSWORD)

    # 10. Click Log In
    page.get_by_role("button", name="Log In").click()

    # 11. Verify successful login by checking URL or page title
    expect(page).not_to_have_url(re.compile(".*login.*"))
