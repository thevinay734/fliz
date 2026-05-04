import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from config.config import BASE_URL


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}login"

    def navigate(self):
        self.goto(self.url)
        expect(self.page).to_have_url(re.compile(".*login.*"))

    # --- Direct login page ---

    def fill_phone(self, phone: str):
        self.page.get_by_placeholder("Phone number").fill(phone)

    def fill_password(self, password: str):
        self.page.get_by_placeholder("Password").fill(password)

    def click_login(self):
        self.page.get_by_role("button", name=re.compile("Login|Sign In|Log in", re.IGNORECASE)).click()

    def login(self, phone: str, password: str):
        self.navigate()
        self.fill_phone(phone)
        self.fill_password(password)
        self.click_login()

    # --- Modal login ---

    def select_country_india(self):
        self.page.get_by_role("button", name="Saudi Arabia: +").click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("searchbox", name="Search country").fill("ind")
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("India", exact=True).click()
        self.page.wait_for_timeout(1000)

    def fill_phone_modal(self, phone: str):
        self.page.get_by_role("textbox", name="Member Phone Number").fill(phone)
        self.page.wait_for_timeout(1000)

    def fill_password_modal(self, password: str):
        self.page.get_by_role("textbox", name="Enter Your Password").fill(password)
        self.page.wait_for_timeout(1000)

    def click_log_in_modal(self):
        self.page.get_by_role("button", name="Log In").click()
        self.page.wait_for_timeout(3000)

    def login_via_modal(self, phone: str, password: str):
        self.select_country_india()
        self.fill_phone_modal(phone)
        self.fill_password_modal(password)
        self.click_log_in_modal()

    # --- Validation ---

    def expect_error_visible(self):
        error_message = self.page.locator("text=/invalid|incorrect|wrong|error/i")
        expect(error_message).to_be_visible()

    def expect_not_on_login_page(self):
        expect(self.page).not_to_have_url(re.compile(".*login.*"))
