import random
import re
import time

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
def test_create_booking_full_flow(page: Page):
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

    # 5. Open country code selector
    page.get_by_role("button", name="Saudi Arabia: +").click()
    time.sleep(1)

    # 6. Search for India
    page.get_by_role("searchbox", name="Search country").fill("ind")
    time.sleep(1)

    # 7. Select India
    page.get_by_text("India", exact=True).click()
    time.sleep(1)

    # 8. Enter phone number
    page.get_by_role("textbox", name="Member Phone Number").fill("+91 97943-05933")
    time.sleep(1)

    # 9. Enter password
    page.get_by_role("textbox", name="Enter Your Password").fill("Vinay@12345")
    time.sleep(1)

    # 10. Click Log In
    page.get_by_role("button", name="Log In").click()
    time.sleep(3)

    # 11. Navigate to page 3
    page.get_by_role("button", name="Page 3").click()
    time.sleep(1)

    # 12. Select company "Rocks 5 Price"
    page.get_by_role("link", name="Rocks 5 Price").click()
    time.sleep(2)

    # 13. Select first available slot
    page.get_by_text(re.compile(r"Available.*")).first.click()
    time.sleep(1)

    # 14. Click Continue
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)

    # 15. Increase quantity
    page.get_by_role("img", name="plus").click()
    time.sleep(1)

    # 16. Open date picker
    page.locator("div").filter(has_text=re.compile(r"^Select start date & time$")).nth(2).click()
    time.sleep(1)

    # 17. Select first enabled available date (skip disabled past dates)
    page.locator("[role='option']:not([aria-disabled='true'])").first.click()
    time.sleep(1)

    # 18. Enter duration
    page.locator("#duration").fill("2")
    time.sleep(1)

    # 19. Click Day dropdown
    page.locator("div").filter(has_text=re.compile(r"^Day$")).nth(3).click()
    time.sleep(1)

    # 20. Select Week
    page.get_by_role("option", name="Week").click()
    time.sleep(1)

    # 21. Clear and fill address
    address_field = page.get_by_role("combobox", name="Alamal Plaza Hail Street..")
    address_field.click()
    time.sleep(1)
    address_field.press("ControlOrMeta+a")
    address_field.fill("noida")
    time.sleep(1)

    # 22. Select Noida address
    page.get_by_role("option", name="Noida, Uttar Pradesh, India", exact=True).click()
    time.sleep(1)

    # 23. Check first agreement checkbox
    page.get_by_role("img", name="unchecked button").first.click()
    time.sleep(1)

    # 24. Handle Rental Contracts popup
    with page.expect_popup() as page1_info:
        page.locator("label").filter(has_text="Rental Contracts").click()
    page1 = page1_info.value
    time.sleep(2)
    page1.close()
    time.sleep(1)

    # 25. Check second checkbox
    page.get_by_role("img", name="unchecked button").click()
    time.sleep(1)

    # 26. Open payment method dropdown
    page.locator("div:nth-child(2) > .flex.items-center.justify-between > .relative > .absolute.bg-black").click()
    time.sleep(1)

    # 27. Click Continue
    page.get_by_role("button", name="Continue").click()
    time.sleep(2)

    # 28. Select payment spans (force to bypass radio overlay)
    page.locator("span").nth(4).click(force=True)
    time.sleep(1)
    page.locator("span").nth(5).click(force=True)
    time.sleep(1)

    # 29. Open final payment dropdown
    page.locator(".flex.items-center.gap-3 > .relative > .absolute.bg-black").click(force=True)
    time.sleep(1)

    # 30. Click Pay now
    page.get_by_role("button", name="Pay now").click()
    time.sleep(2)

    # 31. Click Pay inside iframe
    iframe = page.locator("iframe[name='registrations-target']")
    iframe.content_frame.get_by_role("button", name="Pay").click()
    time.sleep(3)

    # 32. Wait to see final page
    time.sleep(5)
