import random

from faker import Faker

from core.settings import settings
from factories.address_factory import AddressFactory

fake = Faker()


class UserFactory:
    """Generates unique user data for login, signup, and profile tests."""

    @staticmethod
    def create(country: str = "india") -> dict:
        phone = str(random.randint(7000000000, 9999999999))
        address = AddressFactory.create(country)
        return {
            "name": fake.name(),
            "role": "user",
            "email": f"test{random.randint(100000, 999999)}@yopmail.com",
            "phoneNumber": phone,
            "countryCode": "+91" if country.lower() == "india" else "+966",
            "password": settings.LOGIN_PASSWORD,
            **address,
        }

    @staticmethod
    def valid_login() -> dict:
        return {
            "countryCode": settings.LOGIN_COUNTRY_CODE,
            "phoneNumber": settings.LOGIN_PHONE,
            "role": "user",
            "password": settings.LOGIN_PASSWORD,
        }

    @staticmethod
    def invalid_login() -> dict:
        return {
            "countryCode": "+91",
            "phoneNumber": "0000000000",
            "role": "user",
            "password": "wrongpassword",
        }

    @staticmethod
    def signup_payload(country: str = "india", overrides: dict = None) -> dict:
        payload = UserFactory.create(country)
        if overrides:
            payload.update(overrides)
        return payload
