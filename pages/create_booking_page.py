import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from config.config import BASE_URL


class CreateBookingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    # --- Navigation & Language ---

    def open_companies_page(self):
        self.goto(f"{BASE_URL}ar/renter/companies")
        self.page.wait_for_timeout(2000)

    def switch_to_english(self):
        self.page.locator("img").nth(3).click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("English").click()
        self.page.wait_for_timeout(1000)

    # --- Sign in link ---

    def click_sign_in(self):
        self.page.get_by_role("link", name="Sign In").click()
        self.page.wait_for_timeout(1000)

    # --- Company selection ---

    def go_to_pagination_page(self, page_number: str):
        self.page.get_by_role("button", name=f"Page {page_number}").click()
        self.page.wait_for_timeout(1000)

    def select_company(self, name: str):
        self.page.get_by_role("link", name=name).click()
        self.page.wait_for_timeout(2000)

    def select_first_available_slot(self):
        self.page.get_by_text(re.compile(r"Available.*")).first.click()
        self.page.wait_for_timeout(1000)

    def click_continue(self):
        self.page.get_by_role("button", name="Continue").click()
        self.page.wait_for_timeout(2000)

    # --- Booking form ---

    def increase_quantity(self):
        self.page.get_by_role("img", name="plus").click()
        self.page.wait_for_timeout(1000)

    def select_start_date_first_enabled(self):
        self.page.locator("div").filter(
            has_text=re.compile(r"^Select start date & time$")
        ).nth(2).click()
        self.page.wait_for_timeout(1000)
        self.page.locator("[role='option']:not([aria-disabled='true'])").first.click()
        self.page.wait_for_timeout(1000)

    def enter_duration(self, duration: str):
        self.page.locator("#duration").fill(duration)
        self.page.wait_for_timeout(1000)

    def select_duration_unit(self, unit: str):
        self.page.locator("div").filter(has_text=re.compile(r"^Day$")).nth(3).click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("option", name=unit).click()
        self.page.wait_for_timeout(1000)

    def enter_and_select_address(self, query: str, exact_option: str):
        address_field = self.page.get_by_role("combobox", name="Alamal Plaza Hail Street..")
        address_field.click()
        self.page.wait_for_timeout(1000)
        address_field.press("ControlOrMeta+a")
        address_field.fill(query)
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("option", name=exact_option, exact=True).click()
        self.page.wait_for_timeout(1000)

    def check_agreement(self, index: int = 0):
        if index == 0:
            self.page.get_by_role("img", name="unchecked button").first.click()
        else:
            self.page.get_by_role("img", name="unchecked button").click()
        self.page.wait_for_timeout(1000)

    def open_rental_contracts_popup(self):
        with self.page.expect_popup() as page1_info:
            self.page.locator("label").filter(has_text="Rental Contracts").click()
        popup = page1_info.value
        self.page.wait_for_timeout(2000)
        popup.close()
        self.page.wait_for_timeout(1000)

    # --- Payment ---

    def open_payment_method_dropdown(self):
        self.page.locator(
            "div:nth-child(2) > .flex.items-center.justify-between > .relative > .absolute.bg-black"
        ).click()
        self.page.wait_for_timeout(1000)

    def select_payment_span(self, nth: int):
        self.page.locator("span").nth(nth).click(force=True)
        self.page.wait_for_timeout(1000)

    def open_final_payment_dropdown(self):
        self.page.locator(
            ".flex.items-center.gap-3 > .relative > .absolute.bg-black"
        ).click(force=True)
        self.page.wait_for_timeout(1000)

    def click_pay_now(self):
        self.page.get_by_role("button", name="Pay now").click()
        self.page.wait_for_timeout(2000)

    def complete_payment(self):
        iframe = self.page.locator("iframe[name='registrations-target']")
        iframe.content_frame.get_by_role("button", name="Pay").click()
        self.page.wait_for_timeout(3000)

    def wait_for_final_page(self, seconds: int = 5):
        self.page.wait_for_timeout(seconds * 1000)
