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
