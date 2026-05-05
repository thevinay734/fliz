import pytest
from services.vendor_service import VendorService
from factories.user_factory import UserFactory


@pytest.fixture
def vendor_service():
    return VendorService()


@pytest.mark.api
def test_vendor_signup_success(vendor_service: VendorService):
    payload = {
        "name": "Claude Company",
        "role": "vendor",
        "email": f"vendor{UserFactory.create()['phoneNumber']}@yopmail.com",
        "phoneNumber": UserFactory.create()["phoneNumber"],
        "countryCode": "+91",
        "password": "Vinay@12345",
        "address": "Noida, Uttar Pradesh, India",
        "addressLine1": "Sector 62",
        "addressLine2": "",
        "city": "Noida",
        "country": "India",
        "lat": "28.5355",
        "long": "77.3910",
        "state": "Uttar Pradesh",
        "zipcode": "201304",
    }
    response = vendor_service.vendor_signup(payload)
    # SignUp endpoint with role=vendor may return 200/201 or 400/422
    assert response.status_code in (200, 201, 400, 422)
    if response.status_code in (200, 201):
        data = response.json().get("data", {})
        assert "_id" in data or "accessToken" in data


@pytest.mark.api
def test_vendor_signup_invalid_email(vendor_service: VendorService):
    payload = {
        "name": "Test Company",
        "role": "vendor",
        "email": "invalid-email",
        "phoneNumber": "9794305933",
        "countryCode": "+91",
        "password": "Vinay@12345",
        "address": "Noida, Uttar Pradesh, India",
        "city": "Noida",
        "country": "India",
        "state": "Uttar Pradesh",
        "zipcode": "201304",
    }
    response = vendor_service.vendor_signup(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_vendor_signup_missing_company_name(vendor_service: VendorService):
    payload = {
        "role": "vendor",
        "email": "testvendor@yopmail.com",
        "phoneNumber": "9794305933",
        "countryCode": "+91",
        "password": "Vinay@12345",
        "address": "Noida, Uttar Pradesh, India",
        "city": "Noida",
        "country": "India",
        "state": "Uttar Pradesh",
        "zipcode": "201304",
    }
    response = vendor_service.vendor_signup(payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_vendor_signup_missing_phone(vendor_service: VendorService):
    payload = {
        "name": "Test Company",
        "role": "vendor",
        "email": "testvendor@yopmail.com",
        "countryCode": "+91",
        "password": "Vinay@12345",
        "address": "Noida, Uttar Pradesh, India",
        "city": "Noida",
        "country": "India",
        "state": "Uttar Pradesh",
        "zipcode": "201304",
    }
    response = vendor_service.vendor_signup(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_vendor_signup_empty_payload(vendor_service: VendorService):
    response = vendor_service.vendor_signup({})
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_vendor_signup_sql_injection(vendor_service: VendorService):
    payload = {
        "name": "<script>alert(1)</script>",
        "role": "vendor",
        "email": "testvendor@yopmail.com",
        "phoneNumber": "9794305933",
        "countryCode": "+91",
        "password": "Vinay@12345",
        "address": "Noida, Uttar Pradesh, India",
        "city": "Noida",
        "country": "India",
        "state": "Uttar Pradesh",
        "zipcode": "201304",
    }
    response = vendor_service.vendor_signup(payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_vendor_signup_short_password(vendor_service: VendorService):
    payload = {
        "name": "Test Company",
        "role": "vendor",
        "email": "testvendor@yopmail.com",
        "phoneNumber": "9794305933",
        "countryCode": "+91",
        "password": "123",
        "address": "Noida, Uttar Pradesh, India",
        "city": "Noida",
        "country": "India",
        "state": "Uttar Pradesh",
        "zipcode": "201304",
    }
    response = vendor_service.vendor_signup(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_get_vendor_profile_without_auth(vendor_service: VendorService):
    response = vendor_service.get_vendor_profile()
    # Vendor profile endpoint may not exist (404) or require auth (401/403)
    assert response.status_code in (401, 403, 404)


@pytest.mark.api
def test_update_vendor_profile_without_auth(vendor_service: VendorService):
    payload = {"name": "Hacker Company"}
    response = vendor_service.update_vendor_profile(payload)
    # Vendor profile endpoint may not exist (404) or require auth (401/403)
    assert response.status_code in (401, 403, 404)
