import random
import time

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
def test_signup_full_flow(page: Page):
    # 1. Open website
    page.goto("https://dev.fliz.com.sa/ar/renter/companies")
    time.sleep(2)

    # 2. Click language toggle
    page.locator("img").nth(3).click()
    time.sleep(1)

    # 3. Select English
    page.get_by_text("English").click()
    time.sleep(1)

    # 4. Click Sign In
    page.get_by_role("link", name="Sign In").click()
    time.sleep(1)

    # 5. Click Register
    page.get_by_role("link", name="Register").click()
    time.sleep(1)

    # 6. Fill name
    page.get_by_role("textbox", name="Enter Your Name").click()
    page.get_by_role("textbox", name="Enter Your Name").fill("Raju")
    time.sleep(1)

    # 7. Fill email (unique)
    unique_id = random.randint(100000, 999999)
    page.get_by_role("textbox", name="Enter Your Email").click()
    page.get_by_role("textbox", name="Enter Your Email").fill(f"raju{unique_id}@yopmail.com")
    time.sleep(1)

    # 8. Fill address
    page.get_by_role("combobox", name="Address").click()
    page.get_by_role("combobox", name="Address").fill("Noida")
    page.get_by_role("option", name="Noida, Uttar Pradesh, India", exact=True).click()
    time.sleep(1)

    # 9. Open country code selector
    page.get_by_role("button", name="Saudi Arabia: +").click()
    time.sleep(1)

    # 10. Search for India
    page.get_by_role("searchbox", name="Search country").fill("ind")
    time.sleep(1)

    # 11. Select India (+91)
    page.get_by_role("option", name="India+").click()
    time.sleep(1)

    # 12. Enter phone number (unique)
    phone = f"{random.randint(7000000000, 9999999999)}"
    page.get_by_role("textbox", name="Member Phone Number").click()
    page.get_by_role("textbox", name="Member Phone Number").fill(f"+91 {phone[:5]}-{phone[5:]}")
    time.sleep(1)

    # 13. Enter password
    page.locator("#password").fill("Vinay@12345")
    time.sleep(1)

    # 14. Enter confirm password
    page.locator("#confirmPassword").fill("Vinay@12345")
    time.sleep(1)

    # 15. Click on empty area to blur password fields and dismiss hint
    page.mouse.click(0, 0)
    time.sleep(1)

    # 16. Scroll Register button into view
    register_btn = page.get_by_role("button", name="Register")
    register_btn.scroll_into_view_if_needed()
    time.sleep(1)

    # 17. Check terms checkbox
    page.get_by_role("img", name="unchecked button").click()
    time.sleep(1)

    # 18. Click Register
    register_btn.click()
    time.sleep(3)

    # 18. Verify successful signup (redirected from register page)
    expect(page).not_to_have_url("register", timeout=15000)

    # 19. Wait to see final page before browser closes
    time.sleep(5)
