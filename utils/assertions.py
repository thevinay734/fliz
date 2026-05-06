


from typing import List, Union


class ApiAssertions:
    """Shared assertion helpers for API test validation."""

    @staticmethod
    def assert_status_code(response, expected: Union[int, tuple]):
        if isinstance(expected, int):
            assert response.status_code == expected, (
                f"Expected status {expected}, got {response.status_code}"
            )
        else:
            assert response.status_code in expected, (
                f"Expected status in {expected}, got {response.status_code}"
            )

    @staticmethod
    def assert_response_has_keys(response, keys: List[str]):
        try:
            data = response.json()
        except ValueError:
            raise AssertionError("Response is not valid JSON")
        for key in keys:
            assert key in data, f"Missing key '{key}' in response: {data}"

    @staticmethod
    def assert_access_token_present(response):
        ApiAssertions.assert_response_has_keys(response, ["data"])
        data = response.json()["data"]
        token = data.get("accessToken")
        assert token is not None, f"accessToken missing in response data: {data}"

    @staticmethod
    def assert_content_type_json(response):
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Expected JSON Content-Type, got: {content_type}"
        )

    @staticmethod
    def assert_id_present(response):
        ApiAssertions.assert_response_has_keys(response, ["data"])
        data = response.json()["data"]
        _id = data.get("_id")
        assert _id is not None, f"_id missing in response data: {data}"
