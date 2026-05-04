import logging
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Centralized framework settings loaded from environment variables."""

    # URLs
    BASE_URL: str = field(default_factory=lambda: os.getenv("BASE_URL", "https://dev.fliz.com.sa/"))
    API_BASE_URL: str = field(default_factory=lambda: os.getenv("API_BASE_URL", "https://dev.api.fliz.com.sa/"))

    # Environment
    ENVIRONMENT: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "dev"))

    # Test credentials
    LOGIN_COUNTRY_CODE: str = field(default_factory=lambda: os.getenv("LOGIN_COUNTRY_CODE", "+91"))
    LOGIN_PHONE: str = field(default_factory=lambda: os.getenv("LOGIN_PHONE", "9794305933"))
    LOGIN_PASSWORD: str = field(default_factory=lambda: os.getenv("LOGIN_PASSWORD", "Vinay@12345"))

    # Browser settings
    HEADLESS: bool = field(default_factory=lambda: os.getenv("HEADLESS", "false").lower() == "true")
    BROWSER_TYPE: str = field(default_factory=lambda: os.getenv("BROWSER_TYPE", "chromium"))
    VIEWPORT_WIDTH: int = field(default_factory=lambda: int(os.getenv("VIEWPORT_WIDTH", "1280")))
    VIEWPORT_HEIGHT: int = field(default_factory=lambda: int(os.getenv("VIEWPORT_HEIGHT", "720")))

    # Timeouts
    DEFAULT_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("DEFAULT_TIMEOUT", "30000")))
    NAVIGATION_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("NAVIGATION_TIMEOUT", "30000")))
    API_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("API_TIMEOUT", "30")))

    # Logging
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    LOG_DIR: str = field(default_factory=lambda: os.getenv("LOG_DIR", "logs"))

    # Reporting
    ALLURE_RESULTS_DIR: str = field(default_factory=lambda: os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results"))

    # Retry
    MAX_RETRIES: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "3")))
    RETRY_BACKOFF: int = field(default_factory=lambda: int(os.getenv("RETRY_BACKOFF", "2")))

    def get_full_login_phone(self) -> str:
        """Returns formatted phone with country code."""
        return f"{self.LOGIN_COUNTRY_CODE} {self.LOGIN_PHONE[:5]}-{self.LOGIN_PHONE[5:]}"


# Singleton instance
settings = Settings()
