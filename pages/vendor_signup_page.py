from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class VendorSignupPage(BasePage):
    """Page Object for Vendor/Company Provider Signup."""

    def __init__(self, page: Page):
        super().__init__(page)

    # --- Navigation ---

    def click_sign_in(self):
        self.page.get_by_role("link", name="Sign In").click()
        self.page.wait_for_timeout(2000)

    def click_company_provider_tab(self):
        tab = self.page.get_by_role("link", name="Company Provider")
        expect(tab).to_be_visible(timeout=10000)
        tab.click()
        self.page.wait_for_timeout(2000)

    def click_register_link(self):
        # Original codegen: get_by_role("heading", name="Don’t have an account?").get_by_role("link").click()
        # Using regex to handle curly apostrophe
        import re
        heading = self.page.get_by_role("heading", name=re.compile(r"Don.*t have an account\?"))
        if heading.count() > 0:
            link = heading.get_by_role("link")
            if link.count() > 0:
                link.click()
                self.page.wait_for_timeout(2000)

    def click_step_indicator(self):
        indicator = self.page.locator(".absolute.-left-\\[7px\\]")
        if indicator.count() > 0:
            indicator.click()
            self.page.wait_for_timeout(1000)

    # --- Company info ---

    def enter_company_name(self, name: str):
        field = self.page.get_by_role("textbox", name="Enter your Company Name")
        expect(field).to_be_visible(timeout=10000)
        field.fill(name)

    def enter_email(self, email: str):
        field = self.page.get_by_role("textbox", name="Enter Your Email")
        expect(field).to_be_visible(timeout=10000)
        field.fill(email)

    def enter_address(self, query: str, exact_option: str):
        combo = self.page.get_by_role("combobox", name="Address")
        expect(combo).to_be_visible(timeout=10000)
        combo.click()
        combo.fill(query)
        option = self.page.get_by_role("option", name=exact_option, exact=True)
        expect(option).to_be_visible(timeout=10000)
        option.click()

    # --- Country & Phone ---

    def select_country_india(self):
        btn = self.page.get_by_role("button", name="Saudi Arabia: +")
        expect(btn).to_be_visible(timeout=10000)
        btn.click()
        self.page.wait_for_timeout(1000)
        search = self.page.get_by_role("searchbox", name="search")
        expect(search).to_be_visible(timeout=10000)
        search.fill("ind")
        self.page.wait_for_timeout(1000)
        india = self.page.get_by_text("India", exact=True)
        expect(india).to_be_visible(timeout=10000)
        india.click()
        self.page.wait_for_timeout(1000)

    def enter_phone(self, phone: str):
        field = self.page.get_by_role("textbox", name="Member Phone Number")
        expect(field).to_be_visible(timeout=10000)
        field.fill(phone)

    # --- Document Upload (6 documents total) ---

    def upload_document(self, file_path: str):
        """Upload the first generic 'Upload Document'."""
        file_input = self.page.locator("input[type='file']").nth(0)
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(file_path)

    def upload_document_generic(self, file_path: str):
        """Upload the second generic 'Upload Document'."""
        file_input = self.page.locator("input[type='file']").nth(1)
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(file_path)

    def upload_back_side_first(self, file_path: str):
        """Upload Document Back Side (first instance)."""
        file_input = self.page.locator("input[type='file']").nth(2)
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(file_path)

    def upload_front_side(self, file_path: str):
        """Upload Front Side."""
        file_input = self.page.locator("input[type='file']").nth(3)
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(file_path)

    def upload_back_side_second(self, file_path: str):
        """Upload Document Back Side (second instance)."""
        file_input = self.page.locator("input[type='file']").nth(4)
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(file_path)

    def upload_document_third(self, file_path: str):
        """Upload the third generic 'Upload Document'."""
        file_input = self.page.locator("input[type='file']").nth(5)
        expect(file_input).to_be_attached(timeout=10000)
        file_input.set_input_files(file_path)

    # --- Other fields ---

    def enter_message(self, message: str):
        field = self.page.locator("#messageEn")
        expect(field).to_be_visible(timeout=10000)
        field.fill(message)

    def enter_password(self, password: str):
        field = self.page.locator("#password")
        expect(field).to_be_visible(timeout=10000)
        field.fill(password)

    def enter_confirm_password(self, password: str):
        field = self.page.locator("[id=\"confirm Password\"]")
        expect(field).to_be_visible(timeout=10000)
        field.fill(password)

    def check_terms(self):
        self.page.mouse.click(0, 0)
        self.page.wait_for_timeout(500)
        checkbox = self.page.locator(".xl\\:w-7.w-5.h-5.mt-1.block").first
        expect(checkbox).to_be_visible(timeout=10000)
        checkbox.click(force=True)

    def click_register(self):
        btn = self.page.get_by_role("button", name="Register")
        expect(btn).to_be_visible(timeout=10000)
        btn.click()

    # --- Full flow ---

    def signup_as_vendor(self, company_name: str, email: str, address_query: str,
                         address_option: str, phone: str, message: str,
                         password: str, document_path: str = None):
        self.click_sign_in()
        self.click_company_provider_tab()
        self.click_register_link()
        self.click_step_indicator()
        self.enter_company_name(company_name)
        self.enter_email(email)
        self.enter_address(address_query, address_option)
        self.select_country_india()
        self.enter_phone(phone)
        if document_path:
            # Upload all 6 documents with the same dummy file
            self.upload_document(document_path)
            self.upload_document_generic(document_path)
            self.upload_document_third(document_path)
            self.upload_back_side_first(document_path)
            self.upload_front_side(document_path)
            self.upload_back_side_second(document_path)
        self.enter_message(message)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.check_terms()
        self.click_register()
