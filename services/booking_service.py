from services.base_service import BaseService


class BookingService(BaseService):
    """Handles booking API calls."""

    def create_booking(self, payload: dict):
        return self.post("api/v1/renter/bookings", data=payload)

    def get_bookings(self):
        return self.get("api/v1/renter/bookings")

    def get_booking_by_id(self, booking_id: str):
        return self.get(f"api/v1/renter/bookings/{booking_id}")

    def cancel_booking(self, booking_id: str):
        return self.put(f"api/v1/renter/bookings/{booking_id}/cancel")

    def update_booking(self, booking_id: str, payload: dict):
        return self.put(f"api/v1/renter/bookings/{booking_id}", data=payload)
