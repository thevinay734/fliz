import requests
from urllib.parse import urljoin
from config.config import API_BASE_URL

_session = requests.Session()


def _get_url(endpoint: str) -> str:
    return urljoin(API_BASE_URL, endpoint.lstrip("/"))


def get(endpoint, headers=None):
    return _session.get(_get_url(endpoint), headers=headers)


def post(endpoint, data=None, headers=None):
    return _session.post(_get_url(endpoint), json=data, headers=headers)


def put(endpoint, data=None, headers=None):
    return _session.put(_get_url(endpoint), json=data, headers=headers)


def delete(endpoint, headers=None):
    return _session.delete(_get_url(endpoint), headers=headers)

