from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def wait_for_url(self, pattern: str):
        import re
        from playwright.sync_api import expect
        expect(self.page).to_have_url(re.compile(pattern))
