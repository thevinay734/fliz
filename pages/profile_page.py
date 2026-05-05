from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class ProfilePage(BasePage):
    """Page Object for User Profile section."""

    def __init__(self, page: Page):
        super().__init__(page)

    # --- Navigation ---

    def open_profile_menu(self):
        self.page.get_by_role("img", name="profile-menu").click()

    def click_my_profile(self):
        self.page.get_by_role("link", name="My Profile").click()

    def click_edit_profile(self):
        self.page.get_by_role("link", name="Edit Profile").click()

    # --- Form fields ---

    def enter_name(self, name: str):
        field = self.page.get_by_role("textbox", name="Enter your name")
        field.click()
        field.fill(name)

    def enter_email(self, email: str):
        field = self.page.get_by_role("textbox", name="Enter your email")
        field.click()
        field.fill(email)

    def enter_address(self, query: str, exact_option: str):
        combo = self.page.get_by_role("combobox", name="Address")
        combo.click()
        combo.fill(query)
        self.page.get_by_role("option", name=exact_option).click()

    # --- Image upload ---

    def upload_profile_picture(self, file_path: str):
        self.page.locator(".w-8").click()
        self.page.locator("body").set_input_files(file_path)

    # --- Actions ---

    def click_update_profile(self):
        self.page.get_by_role("button", name="Update Profile").click()

    def navigate_back_to_home(self):
        self.page.get_by_role("paragraph").filter(has_text="Home/My Profile").get_by_role("link").click()

    # --- Full flow ---

    def update_profile(self, name: str, email: str, address_query: str,
                       address_option: str, image_path: str = None):
        self.open_profile_menu()
        self.click_my_profile()
        self.click_edit_profile()
        self.enter_name(name)
        self.enter_email(email)
        self.enter_address(address_query, address_option)
        if image_path:
            self.upload_profile_picture(image_path)
        self.click_update_profile()
