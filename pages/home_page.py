import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from config.config import BASE_URL


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = BASE_URL

    def navigate(self):
        self.goto(self.url)

    def expect_title_contains_fliz(self):
        expect(self.page).to_have_title(re.compile("Fliz"))

    def expect_url_contains_fliz(self):
        expect(self.page).to_have_url(re.compile(".*fliz.*"))

    def click_language_toggle(self):
        self.page.locator("img").nth(3).click()

    def select_english(self):
        self.page.get_by_text("English").click()

    def click_sign_in(self):
        self.page.get_by_role("link", name="Sign In").click()

    def open_sign_in_modal(self):
        self.click_language_toggle()
        self.select_english()
        self.click_sign_in()
