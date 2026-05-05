import pytest

from services.auth_service import AuthService
from services.user_service import UserService


@pytest.fixture
def user_service(authenticated_auth_service):
    """Fixture that returns a UserService with auth token already set."""
    service = UserService(authenticated_auth_service.client)
    return service


@pytest.mark.api
def test_get_profile(user_service: UserService):
    response = user_service.get_profile()
    assert response.status_code == 200
    data = response.json().get("data", {})
    assert "name" in data or "email" in data or "_id" in data


@pytest.mark.api
def test_update_profile_name(user_service: UserService):
    payload = {"name": "Rajesh Sharma"}
    response = user_service.update_profile(payload)
    assert response.status_code in (200, 201)


@pytest.mark.api
def test_update_profile_email(user_service: UserService):
    payload = {"email": "rajesh@test.com"}
    response = user_service.update_profile(payload)
    assert response.status_code in (200, 201, 400)


@pytest.mark.api
def test_update_profile_address(user_service: UserService):
    payload = {
        "address": "Noida, Uttar Pradesh, India",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "country": "India",
    }
    response = user_service.update_profile(payload)
    assert response.status_code in (200, 201)


@pytest.mark.api
def test_update_profile_empty_name(user_service: UserService):
    payload = {"name": ""}
    response = user_service.update_profile(payload)
    assert response.status_code in (400, 422)


@pytest.mark.api
def test_update_profile_invalid_email(user_service: UserService):
    payload = {"email": "not-an-email"}
    response = user_service.update_profile(payload)
    assert response.status_code in (400, 422)


@pytest.mark.api
def test_update_profile_xss_payload(user_service: UserService):
    payload = {"name": "<script>alert(1)</script>"}
    response = user_service.update_profile(payload)
    assert response.status_code in (200, 400, 422)


@pytest.mark.api
def test_update_profile_sql_injection(user_service: UserService):
    payload = {"name": "' OR 1=1 --"}
    response = user_service.update_profile(payload)
    assert response.status_code in (200, 400, 422)


@pytest.mark.api
def test_get_profile_without_auth():
    """Profile should not be accessible without token."""
    service = UserService()
    response = service.get_profile()
    assert response.status_code in (401, 403)


@pytest.mark.api
def test_update_profile_without_auth():
    """Update should not work without token."""
    service = UserService()
    payload = {"name": "Hacker"}
    response = service.update_profile(payload)
    assert response.status_code in (401, 403)
