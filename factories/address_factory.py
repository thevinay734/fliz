from faker import Faker

fake = Faker()


class AddressFactory:
    """Generates realistic addresses for different countries."""

    @staticmethod
    def india() -> dict:
        return {
            "address": f"{fake.city()}, {fake.state()}, India",
            "addressLine1": fake.street_address(),
            "addressLine2": "",
            "city": fake.city(),
            "country": "India",
            "state": fake.state(),
            "zipcode": fake.postcode(),
            "lat": str(fake.latitude()),
            "long": str(fake.longitude()),
        }

    @staticmethod
    def saudi_arabia() -> dict:
        return {
            "address": f"{fake.city()}, {fake.state()}, Saudi Arabia",
            "addressLine1": fake.street_address(),
            "addressLine2": "",
            "city": fake.city(),
            "country": "Saudi Arabia",
            "state": fake.state(),
            "zipcode": fake.postcode(),
            "lat": str(fake.latitude()),
            "long": str(fake.longitude()),
        }

    @staticmethod
    def create(country: str = "india") -> dict:
        if country.lower() == "india":
            return AddressFactory.india()
        if country.lower() in ("saudi", "saudi_arabia", "sa"):
            return AddressFactory.saudi_arabia()
        return AddressFactory.india()
