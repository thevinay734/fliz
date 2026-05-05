import random

from faker import Faker

from factories.address_factory import AddressFactory

fake = Faker()


class VendorFactory:
    """Generates unique vendor/company data for signup tests."""

    @staticmethod
    def create(country: str = "india") -> dict:
        phone = str(random.randint(7000000000, 9999999999))
        address = AddressFactory.create(country)
        return {
            "company_name": fake.company(),
            "email": f"vendor{random.randint(100000, 999999)}@yopmail.com",
            "phone": f"+91 {phone[:5]}-{phone[5:]}",
            "address_query": "Noida",
            "address_option": "Noida, Uttar Pradesh, India",
            "message": fake.sentence(),
            "password": "Vinay@12345",
            **address,
        }
