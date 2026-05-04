import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


@pytest.fixture
def home_page(page: Page):
    return HomePage(page)


def test_homepage_has_title(home_page: HomePage):
    home_page.navigate()
    home_page.expect_title_contains_fliz()


def test_homepage_url(home_page: HomePage):
    home_page.navigate()
    home_page.expect_url_contains_fliz()
