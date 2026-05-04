# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python test suite for `https://dev.fliz.com.sa/` supporting both API automation (`pytest` + `requests`) and browser automation (`pytest` + `playwright`).

## Common Commands

Activate the virtual environment before running commands:

```bash
source .venv/bin/activate
```

Run all tests:
```bash
pytest
```

Run a single test file:
```bash
pytest tests/test_login.py
```

Run Playwright tests (headless):
```bash
pytest tests/test_playwright_example.py
```

Run Playwright tests with visible browser:
```bash
pytest tests/test_playwright_example.py --headed
```

Run Playwright tests in headed mode with UI debug:
```bash
pytest tests/test_playwright_example.py --headed --slowmo 1000
```

Debug a Playwright test (stops on failures with inspector):
```bash
pytest tests/test_playwright_example.py --headed --pwdebug
```

## Architecture

- **`config/config.py`** defines `BASE_URL`.
- **`utils/api_client.py`** provides thin `get(endpoint, ...)` and `post(endpoint, ...)` wrappers around `requests` that automatically prefix `BASE_URL`. Prefer using these helpers in tests instead of calling `requests` directly, so endpoint paths stay relative and the base URL remains centralized.
- **`tests/`** uses plain `pytest` functions.
- **Playwright tests** use the `page` fixture from `pytest-playwright` (e.g. `def test_example(page: Page): ...`).
- There is no existing `requirements.txt`; dependencies (`pytest`, `requests`, `playwright`, `pytest-playwright`) are installed in `.venv`.

## Notes

- `tests/test_api.py` is currently empty and appears to be a placeholder.
- `tests/test_login.py` currently imports `requests` directly and hardcodes the full URL; the intended pattern is to import from `utils.api_client` and `config.config`.
