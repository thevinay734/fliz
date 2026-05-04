from core.api_client import api_client
from utils.assertions import ApiAssertions


class BaseService:
    """Base class for all API services."""

    def __init__(self, client=None):
        self.client = client or api_client
        self.assertions = ApiAssertions()

    def get(self, endpoint: str, headers=None):
        return self.client.get(endpoint, headers=headers)

    def post(self, endpoint: str, data=None, headers=None):
        return self.client.post(endpoint, data=data, headers=headers)

    def put(self, endpoint: str, data=None, headers=None):
        return self.client.put(endpoint, data=data, headers=headers)

    def delete(self, endpoint: str, headers=None):
        return self.client.delete(endpoint, headers=headers)
