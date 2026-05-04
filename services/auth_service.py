from typing import Optional

from core.api_client import api_client
from factories.user_factory import UserFactory
from services.base_service import BaseService


class AuthService(BaseService):
    """Handles authentication API calls and token management."""

    def __init__(self, client=None):
        super().__init__(client)
        self._token: Optional[str] = None

    # --- Auth API calls ---

    def login(self, payload: dict):
        response = self.post("api/v1/common/auth/login", data=payload)
        if response.status_code == 200:
            try:
                token = response.json()["data"]["accessToken"]
                self.set_token(token)
            except (KeyError, ValueError):
                pass
        return response

    def signup(self, payload: dict):
        return self.post("api/v1/common/auth/signUp", data=payload)

    def logout(self):
        return self.post("api/v1/common/auth/logout")

    # --- Token management ---

    def set_token(self, token: str):
        self._token = token
        self.client.set_auth_token(token)

    def clear_token(self):
        self._token = None
        self.client.clear_auth_token()

    # --- Payload factories ---

    @staticmethod
    def get_login_payload(overrides: dict = None) -> dict:
        payload = UserFactory.valid_login()
        if overrides:
            payload.update(overrides)
        return payload

    @staticmethod
    def get_signup_payload(country: str = "india", overrides: dict = None) -> dict:
        payload = UserFactory.signup_payload(country, overrides)
        return payload
