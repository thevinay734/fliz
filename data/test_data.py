import os
from dotenv import load_dotenv

load_dotenv()

LOGIN_PAYLOAD = {
    "countryCode": os.getenv("LOGIN_COUNTRY_CODE", "+91"),
    "phoneNumber": os.getenv("LOGIN_PHONE", "9794305933"),
    "role": "user",
    "password": os.getenv("LOGIN_PASSWORD", "Vinay@12345"),
}

INVALID_LOGIN_PAYLOAD = {
    "countryCode": "+91",
    "phoneNumber": "0000000000",
    "role": "user",
    "password": "wrongpassword",
}

SIGNUP_PAYLOAD = {
    "name": "Vinay",
    "role": "user",
    "email": "flizadmin@gmail.com",
    "phoneNumber": "9219581219",
    "countryCode": "+91",
    "password": "Vinay@12345",
    "address": "Noida, Uttar Pradesh, India",
    "addressLine1": "",
    "addressLine2": "",
    "city": "Noida",
    "country": "India",
    "lat": "28.5355161",
    "long": "77.3910265",
    "state": "Uttar Pradesh",
    "zipcode": "201304",
}

INVALID_SIGNUP_PAYLOAD = {
    "name": "",
    "role": "user",
    "email": "invalid-email",
    "phoneNumber": "0000000000",
    "countryCode": "+91",
    "password": "123",
    "address": "",
    "city": "",
    "country": "",
    "state": "",
    "zipcode": "",
}
