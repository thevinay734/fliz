import pytest

from pages.create_booking_page import CreateBookingPage
from pages.login_page import LoginPage


@pytest.mark.ui
def test_create_booking_full_flow(booking_page: CreateBookingPage, login_page: LoginPage):
    # 1. Open website and switch language
    booking_page.open_companies_page()
    booking_page.switch_to_english()

    # 2. Log in via modal
    booking_page.click_sign_in()
    login_page.login_via_modal("+91 97943-05933", "Vinay@12345")

    # 3. Navigate to page 3 and select company
    booking_page.go_to_pagination_page("3")
    booking_page.select_company("Rocks 5 Price")

    # 4. Select slot and continue
    booking_page.select_first_available_slot()
    booking_page.click_continue()

    # 5. Fill booking form
    booking_page.increase_quantity()
    booking_page.select_start_date_first_enabled()
    booking_page.enter_duration("2")
    booking_page.select_duration_unit("Week")
    booking_page.enter_and_select_address("noida", "Noida, Uttar Pradesh, India")

    # 6. Agreements
    booking_page.check_agreement(index=0)
    booking_page.open_rental_contracts_popup()
    booking_page.check_agreement(index=1)

    # 7. Payment flow
    booking_page.open_payment_method_dropdown()
    booking_page.click_continue()
    booking_page.select_payment_span(4)
    booking_page.select_payment_span(5)
    booking_page.open_final_payment_dropdown()
    booking_page.click_pay_now()
    booking_page.complete_payment()

    # 8. Wait to see final page
    booking_page.wait_for_final_page(5)
