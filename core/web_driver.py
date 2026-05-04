from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from core.settings import settings


class WebDriver:
    """Browser factory for Playwright with configurable options."""

    _playwright: Playwright | None = None
    _browser: Browser | None = None

    @classmethod
    def get_playwright(cls) -> Playwright:
        if cls._playwright is None:
            cls._playwright = sync_playwright().start()
        return cls._playwright

    @classmethod
    def launch_browser(cls, browser_type: str = None, headless: bool = None) -> Browser:
        pw = cls.get_playwright()
        browser_type = browser_type or settings.BROWSER_TYPE
        headless = headless if headless is not None else settings.HEADLESS

        launch_options = {"headless": headless}

        if browser_type == "chromium":
            return pw.chromium.launch(**launch_options)
        elif browser_type == "firefox":
            return pw.firefox.launch(**launch_options)
        elif browser_type == "webkit":
            return pw.webkit.launch(**launch_options)
        else:
            return pw.chromium.launch(**launch_options)

    @classmethod
    def new_context(cls, browser: Browser = None, tracing: bool = False) -> BrowserContext:
        browser = browser or cls.launch_browser()
        context_options = {
            "viewport": {
                "width": settings.VIEWPORT_WIDTH,
                "height": settings.VIEWPORT_HEIGHT,
            }
        }
        context = browser.new_context(**context_options)
        if tracing:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
        return context

    @classmethod
    def new_page(cls, browser: Browser = None, tracing: bool = False) -> Page:
        context = cls.new_context(browser, tracing)
        return context.new_page()

    @classmethod
    def stop(cls):
        if cls._browser:
            cls._browser.close()
            cls._browser = None
        if cls._playwright:
            cls._playwright.stop()
            cls._playwright = None
