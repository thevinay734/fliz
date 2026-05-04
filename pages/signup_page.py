import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from config.config import BASE_URL


class SignUpPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}ar/renter/companies"

    # --- Navigation & Language ---

    def open(self):
        self.goto(self.url)
        self.page.wait_for_timeout(2000)

    def switch_to_english(self):
        self.page.locator("img").nth(3).click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("English").click()
        self.page.wait_for_timeout(1000)

    def open_sign_in_modal(self):
        self.page.get_by_role("link", name="Sign In").click()
        self.page.wait_for_timeout(1000)

    def click_register(self):
        self.page.get_by_role("link", name="Register").click()
        self.page.wait_for_timeout(1000)

    # --- Registration form ---

    def enter_name(self, name: str):
        self.page.get_by_role("textbox", name="Enter Your Name").fill(name)
        self.page.wait_for_timeout(1000)

    def enter_email(self, email: str):
        self.page.get_by_role("textbox", name="Enter Your Email").fill(email)
        self.page.wait_for_timeout(1000)

    def enter_address(self, query: str, exact_option: str):
        combo = self.page.get_by_role("combobox", name="Address")
        combo.click()
        combo.fill(query)
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("option", name=exact_option, exact=True).click()
        self.page.wait_for_timeout(1000)

    def select_country_india(self):
        self.page.get_by_role("button", name="Saudi Arabia: +").click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("searchbox", name="Search country").fill("ind")
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("option", name="India+").click()
        self.page.wait_for_timeout(1000)

    def enter_phone(self, phone: str):
        self.page.get_by_role("textbox", name="Member Phone Number").fill(phone)
        self.page.wait_for_timeout(1000)

    def enter_password(self, password: str):
        self.page.locator("#password").fill(password)
        self.page.wait_for_timeout(1000)

    def enter_confirm_password(self, password: str):
        self.page.locator("#confirmPassword").fill(password)
        self.page.wait_for_timeout(1000)

    def dismiss_password_hint(self):
        self.page.mouse.click(0, 0)
        self.page.wait_for_timeout(1000)

    def check_terms(self):
        self.page.get_by_role("img", name="unchecked button").click()
        self.page.wait_for_timeout(1000)

    def click_register_button(self):
        btn = self.page.get_by_role("button", name="Register")
        btn.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        btn.click()
        self.page.wait_for_timeout(3000)

    # --- Flow helpers ---

    def register(self, name: str, email: str, address_query: str,
                 address_option: str, phone: str, password: str):
        self.open()
        self.switch_to_english()
        self.open_sign_in_modal()
        self.click_register()
        self.enter_name(name)
        self.enter_email(email)
        self.enter_address(address_query, address_option)
        self.select_country_india()
        self.enter_phone(phone)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.dismiss_password_hint()
        self.check_terms()
        self.click_register_button()

    def expect_not_on_register_page(self, timeout: int = 15000):
        expect(self.page).not_to_have_url("register", timeout=timeout)
