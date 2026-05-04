import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()


class BookingFactory:
    """Generates realistic booking data."""

    @staticmethod
    def create() -> dict:
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        duration = random.randint(1, 4)
        unit = random.choice(["day", "week", "month"])

        return {
            "quantity": random.randint(1, 5),
            "startDate": start_date.strftime("%Y-%m-%d"),
            "duration": duration,
            "durationUnit": unit,
            "address": f"{fake.city()}, {fake.state()}, India",
            "notes": fake.sentence(),
        }

    @staticmethod
    def with_custom_date(days_from_now: int = 7) -> dict:
        start_date = datetime.now() + timedelta(days=days_from_now)
        return {
            "quantity": 1,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "duration": 2,
            "durationUnit": "week",
            "address": f"{fake.city()}, {fake.state()}, India",
            "notes": "Custom date booking",
        }
