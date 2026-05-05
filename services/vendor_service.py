from services.base_service import BaseService


class VendorService(BaseService):
    """Handles vendor/company provider API calls."""

    def vendor_signup(self, payload: dict):
        # Vendor signup likely uses the same endpoint as user signup
        # with role="vendor"
        return self.post("api/v1/common/auth/signUp", data=payload)

    def get_vendor_profile(self):
        return self.get("api/v1/vendor/me")

    def update_vendor_profile(self, payload: dict):
        return self.put("api/v1/vendor/profile", data=payload)

    def upload_vendor_document(self, files: dict):
        return self.post("api/v1/vendor/documents", files=files)
