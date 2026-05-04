import random

import pytest

from pages.signup_page import SignUpPage


@pytest.fixture
def signup_page(page):
    return SignUpPage(page)


@pytest.mark.ui
def test_signup_full_flow(signup_page: SignUpPage):
    unique_id = random.randint(100000, 999999)
    email = f"raju{unique_id}@yopmail.com"
    phone = f"{random.randint(7000000000, 9999999999)}"
    formatted_phone = f"+91 {phone[:5]}-{phone[5:]}"

    signup_page.register(
        name="Raju",
        email=email,
        address_query="Noida",
        address_option="Noida, Uttar Pradesh, India",
        phone=formatted_phone,
        password="Vinay@12345",
    )
    signup_page.expect_not_on_register_page()
