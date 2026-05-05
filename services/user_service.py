from services.base_service import BaseService


class UserService(BaseService):
    """Handles user profile API calls."""

    def get_profile(self):
        return self.get("api/v1/user/me")

    def update_profile(self, payload: dict):
        return self.put("api/v1/user/profile", data=payload)

    def upload_profile_picture(self, files: dict):
        return self.post("api/v1/user/profile-picture", data={}, files=files)
