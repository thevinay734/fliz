import pytest
from services.auth_service import AuthService


@pytest.mark.api
def test_login_success(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    response = auth_service.login(payload)
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    assert response_json["data"].get("accessToken") is not None


@pytest.mark.api
def test_login_invalid_credentials(auth_service: AuthService):
    payload = auth_service.get_login_payload({
        "phoneNumber": "0000000000",
        "password": "wrongpassword"
    })
    response = auth_service.login(payload)
    assert response.status_code in (400, 401, 403, 404, 422)


@pytest.mark.api
def test_login_missing_country_code(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    del payload["countryCode"]
    response = auth_service.login(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_missing_phone_number(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    del payload["phoneNumber"]
    response = auth_service.login(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_missing_password(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    del payload["password"]
    response = auth_service.login(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_missing_role(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    del payload["role"]
    response = auth_service.login(payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_login_empty_payload(auth_service: AuthService):
    response = auth_service.login({})
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_invalid_country_code_format(auth_service: AuthService):
    payload = auth_service.get_login_payload({"countryCode": "91"})
    response = auth_service.login(payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_login_invalid_phone_format(auth_service: AuthService):
    payload = auth_service.get_login_payload({"phoneNumber": "abcdefghij"})
    response = auth_service.login(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_wrong_role(auth_service: AuthService):
    payload = auth_service.get_login_payload({"role": "admin"})
    response = auth_service.login(payload)
    assert response.status_code in (400, 401, 403, 404, 422)


@pytest.mark.api
def test_login_sql_injection_password(auth_service: AuthService):
    payload = auth_service.get_login_payload({"password": '" OR 1=1 --'})
    response = auth_service.login(payload)
    assert response.status_code in (400, 401, 403, 404, 422)


@pytest.mark.api
def test_login_xss_payload(auth_service: AuthService):
    payload = auth_service.get_login_payload({"phoneNumber": '<script>alert(1)</script>'})
    response = auth_service.login(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_extra_fields(auth_service: AuthService):
    payload = auth_service.get_login_payload({"extraField": "shouldBeIgnored"})
    response = auth_service.login(payload)
    assert response.status_code in (200, 422)
    if response.status_code == 200:
        response_json = response.json()
        assert "data" in response_json


@pytest.mark.api
def test_login_response_structure(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    response = auth_service.login(payload)
    assert response.status_code == 200
    response_json = response.json()
    assert "status" in response_json or "success" in response_json or "data" in response_json
    assert "data" in response_json
    assert response_json["data"].get("accessToken") is not None


@pytest.mark.api
def test_login_content_type_json(auth_service: AuthService):
    payload = auth_service.get_login_payload()
    response = auth_service.login(payload)
    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.api
def test_signup_success(auth_service: AuthService):
    payload = auth_service.get_signup_payload()
    response = auth_service.signup(payload)
    assert response.status_code in (200, 201)
    response_json = response.json()
    assert "data" in response_json


@pytest.mark.api
def test_signup_invalid_email_format(auth_service: AuthService):
    payload = auth_service.get_signup_payload(overrides={"email": "invalid-email"})
    response = auth_service.signup(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_invalid_phone_format(auth_service: AuthService):
    payload = auth_service.get_signup_payload(overrides={"phoneNumber": "abcdefghij"})
    response = auth_service.signup(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_missing_name(auth_service: AuthService):
    payload = auth_service.get_signup_payload()
    del payload["name"]
    response = auth_service.signup(payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_signup_missing_phone(auth_service: AuthService):
    payload = auth_service.get_signup_payload()
    del payload["phoneNumber"]
    response = auth_service.signup(payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_empty_payload(auth_service: AuthService):
    response = auth_service.signup({})
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_sql_injection_name(auth_service: AuthService):
    payload = auth_service.get_signup_payload(overrides={"name": '<script>alert(1)</script>'})
    response = auth_service.signup(payload)
    assert response.status_code in (200, 201, 400, 404, 422)


@pytest.mark.api
def test_signup_response_structure(auth_service: AuthService):
    payload = auth_service.get_signup_payload()
    response = auth_service.signup(payload)
    assert response.status_code in (200, 201)
    response_json = response.json()
    assert "data" in response_json
    assert response_json["data"].get("_id") is not None


@pytest.mark.api
def test_signup_content_type_json(auth_service: AuthService):
    payload = auth_service.get_signup_payload()
    response = auth_service.signup(payload)
    assert response.status_code in (200, 201)
    assert "application/json" in response.headers.get("Content-Type", "")
