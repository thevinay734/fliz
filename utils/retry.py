import functools
import logging
import time

from core.settings import settings

logger = logging.getLogger(__name__)


def retry_on_failure(max_attempts: int = None, backoff: int = None, exceptions: tuple = (Exception,)):
    """Decorator to retry a function on specified exceptions."""
    max_attempts = max_attempts or settings.MAX_RETRIES
    backoff = backoff or settings.RETRY_BACKOFF

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    logger.warning(f"{func.__name__} attempt {attempt}/{max_attempts} failed: {exc}")
                    if attempt == max_attempts:
                        raise
                    sleep_time = backoff * (2 ** (attempt - 1))
                    logger.info(f"Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                    attempt += 1
            return None
        return wrapper
    return decorator


def retry_on_timeout(max_attempts: int = None):
    """Shortcut decorator for timeout/network retries."""
    import requests
    return retry_on_failure(
        max_attempts=max_attempts or settings.MAX_RETRIES,
        exceptions=(requests.ConnectionError, requests.Timeout),
    )
