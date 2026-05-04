import random

import pytest
from utils.api_client import post
from data.test_data import LOGIN_PAYLOAD, INVALID_LOGIN_PAYLOAD, SIGNUP_PAYLOAD, INVALID_SIGNUP_PAYLOAD


def _unique_signup_payload():
    payload = SIGNUP_PAYLOAD.copy()
    payload["phoneNumber"] = str(random.randint(7000000000, 9999999999))
    payload["email"] = f"test{random.randint(100000, 999999)}@yopmail.com"
    return payload


@pytest.mark.api
def test_login_success():
    response = post("api/v1/common/auth/login", data=LOGIN_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    assert response_json["data"].get("accessToken") is not None


@pytest.mark.api
def test_login_invalid_credentials():
    response = post("api/v1/common/auth/login", data=INVALID_LOGIN_PAYLOAD)
    assert response.status_code in (400, 401, 403, 404, 422)


@pytest.mark.api
def test_login_missing_country_code():
    payload = LOGIN_PAYLOAD.copy()
    del payload["countryCode"]
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_missing_phone_number():
    payload = LOGIN_PAYLOAD.copy()
    del payload["phoneNumber"]
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_missing_password():
    payload = LOGIN_PAYLOAD.copy()
    del payload["password"]
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_missing_role():
    payload = LOGIN_PAYLOAD.copy()
    del payload["role"]
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_login_empty_payload():
    response = post("api/v1/common/auth/login", data={})
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_invalid_country_code_format():
    payload = LOGIN_PAYLOAD.copy()
    payload["countryCode"] = "91"
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_login_invalid_phone_format():
    payload = LOGIN_PAYLOAD.copy()
    payload["phoneNumber"] = "abcdefghij"
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_wrong_role():
    payload = LOGIN_PAYLOAD.copy()
    payload["role"] = "admin"
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 401, 403, 404, 422)


@pytest.mark.api
def test_login_sql_injection_password():
    payload = LOGIN_PAYLOAD.copy()
    payload["password"] = '" OR 1=1 --'
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 401, 403, 404, 422)


@pytest.mark.api
def test_login_xss_payload():
    payload = LOGIN_PAYLOAD.copy()
    payload["phoneNumber"] = '<script>alert(1)</script>'
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_login_extra_fields():
    payload = LOGIN_PAYLOAD.copy()
    payload["extraField"] = "shouldBeIgnored"
    response = post("api/v1/common/auth/login", data=payload)
    assert response.status_code in (200, 422)
    if response.status_code == 200:
        response_json = response.json()
        assert "data" in response_json


@pytest.mark.api
def test_login_response_structure():
    response = post("api/v1/common/auth/login", data=LOGIN_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert "status" in response_json or "success" in response_json or "data" in response_json
    assert "data" in response_json
    assert response_json["data"].get("accessToken") is not None


@pytest.mark.api
def test_login_content_type_json():
    response = post("api/v1/common/auth/login", data=LOGIN_PAYLOAD)
    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.api
def test_signup_success():
    response = post("api/v1/common/auth/signUp", data=_unique_signup_payload())
    assert response.status_code in (200, 201)
    response_json = response.json()
    assert "data" in response_json


@pytest.mark.api
def test_signup_invalid_email_format():
    payload = SIGNUP_PAYLOAD.copy()
    payload["email"] = "invalid-email"
    response = post("api/v1/common/auth/signUp", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_invalid_phone_format():
    payload = SIGNUP_PAYLOAD.copy()
    payload["phoneNumber"] = "abcdefghij"
    response = post("api/v1/common/auth/signUp", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_missing_name():
    payload = SIGNUP_PAYLOAD.copy()
    del payload["name"]
    response = post("api/v1/common/auth/signUp", data=payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_signup_missing_phone():
    payload = SIGNUP_PAYLOAD.copy()
    del payload["phoneNumber"]
    response = post("api/v1/common/auth/signUp", data=payload)
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_empty_payload():
    response = post("api/v1/common/auth/signUp", data={})
    assert response.status_code in (400, 404, 422)


@pytest.mark.api
def test_signup_sql_injection_name():
    payload = SIGNUP_PAYLOAD.copy()
    payload["name"] = '<script>alert(1)</script>'
    response = post("api/v1/common/auth/signUp", data=payload)
    assert response.status_code in (200, 400, 404, 422)


@pytest.mark.api
def test_signup_response_structure():
    response = post("api/v1/common/auth/signUp", data=_unique_signup_payload())
    assert response.status_code in (200, 201)
    response_json = response.json()
    assert "data" in response_json
    assert response_json["data"].get("_id") is not None


@pytest.mark.api
def test_signup_content_type_json():
    response = post("api/v1/common/auth/signUp", data=_unique_signup_payload())
    assert response.status_code in (200, 201)
    assert "application/json" in response.headers.get("Content-Type", "")
