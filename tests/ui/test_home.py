import re
from playwright.sync_api import Page, expect
from config.config import BASE_URL


def test_homepage_has_title(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title(re.compile("Fliz"))


def test_homepage_url(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_url(re.compile(".*fliz.*"))
