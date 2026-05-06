import json
import logging
import os
import time
from typing import Callable, Optional
from urllib.parse import urljoin

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from core.settings import settings


def _retry_config():
    return retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_BACKOFF, min=1, max=30),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        reraise=True,
    )


class ApiClient:
    """Enterprise-grade HTTP client with logging, retry, auth, and hooks."""

    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = settings.API_TIMEOUT
        self.base_url = settings.API_BASE_URL
        self._auth_token: Optional[str] = None
        self._logger = logging.getLogger(self.__class__.__name__)

        # Hooks
        self._before_request_hooks: list[Callable] = []
        self._after_response_hooks: list[Callable] = []

        # Ensure log directory exists
        os.makedirs(settings.LOG_DIR, exist_ok=True)

        # File handler for API logs
        fh = logging.FileHandler(os.path.join(settings.LOG_DIR, "api_requests.log"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self._logger.addHandler(fh)
        self._logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # --- Auth ---

    def set_auth_token(self, token: str):
        self._auth_token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_auth_token(self):
        self._auth_token = None
        self.session.headers.pop("Authorization", None)

    # --- Hooks ---

    def add_before_request_hook(self, hook: Callable):
        self._before_request_hooks.append(hook)

    def add_after_response_hook(self, hook: Callable):
        self._after_response_hooks.append(hook)

    # --- Helpers ---

    def _build_url(self, endpoint: str) -> str:
        return urljoin(self.base_url, endpoint.lstrip("/"))

    def _log_request(self, method: str, url: str, data=None, headers=None):
        self._logger.info(f"➡️  {method} {url}")
        if headers:
            self._logger.debug(f"   Headers: {headers}")
        if data:
            try:
                self._logger.debug(f"   Body: {json.dumps(data, indent=2)}")
            except (TypeError, ValueError):
                self._logger.debug(f"   Body: {data}")

    def _log_response(self, response: requests.Response, elapsed_ms: float):
        self._logger.info(f"⬅️  {response.status_code} {response.url} ({elapsed_ms:.0f}ms)")
        try:
            body = response.json()
            self._logger.debug(f"   Response: {json.dumps(body, indent=2)}")
        except ValueError:
            self._logger.debug(f"   Response: {response.text[:500]}")

    def _run_before_hooks(self, method: str, url: str, kwargs: dict):
        for hook in self._before_request_hooks:
            hook(method, url, kwargs)

    def _run_after_hooks(self, response: requests.Response):
        for hook in self._after_response_hooks:
            hook(response)

    # --- HTTP Methods ---

    @_retry_config()
    def get(self, endpoint: str, headers=None, **kwargs):
        url = self._build_url(endpoint)
        kwargs["headers"] = headers
        self._run_before_hooks("GET", url, kwargs)
        self._log_request("GET", url, headers=headers)

        start = time.time()
        response = self.session.get(url, **kwargs)
        elapsed_ms = (time.time() - start) * 1000

        self._log_response(response, elapsed_ms)
        self._run_after_hooks(response)
        return response

    @_retry_config()
    def post(self, endpoint: str, data=None, headers=None, **kwargs):
        url = self._build_url(endpoint)
        kwargs["json"] = data
        kwargs["headers"] = headers
        self._run_before_hooks("POST", url, kwargs)
        self._log_request("POST", url, data=data, headers=headers)

        start = time.time()
        response = self.session.post(url, **kwargs)
        elapsed_ms = (time.time() - start) * 1000

        self._log_response(response, elapsed_ms)
        self._run_after_hooks(response)
        return response

    @_retry_config()
    def put(self, endpoint: str, data=None, headers=None, **kwargs):
        url = self._build_url(endpoint)
        kwargs["json"] = data
        kwargs["headers"] = headers
        self._run_before_hooks("PUT", url, kwargs)
        self._log_request("PUT", url, data=data, headers=headers)

        start = time.time()
        response = self.session.put(url, **kwargs)
        elapsed_ms = (time.time() - start) * 1000

        self._log_response(response, elapsed_ms)
        self._run_after_hooks(response)
        return response

    @_retry_config()
    def delete(self, endpoint: str, headers=None, **kwargs):
        url = self._build_url(endpoint)
        kwargs["headers"] = headers
        self._run_before_hooks("DELETE", url, kwargs)
        self._log_request("DELETE", url, headers=headers)

        start = time.time()
        response = self.session.delete(url, **kwargs)
        elapsed_ms = (time.time() - start) * 1000

        self._log_response(response, elapsed_ms)
        self._run_after_hooks(response)
        return response


# Singleton
api_client = ApiClient()
