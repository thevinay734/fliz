# Fliz Automation Project

Python test suite for `https://dev.fliz.com.sa/` supporting both API and browser automation.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

2. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Project Structure

```
├── config/            # Configuration (BASE_URL, environments)
├── utils/             # API client helpers and shared utilities
├── pages/             # Page Object Models for Playwright UI tests
├── data/              # Test data and payloads
├── tests/
│   ├── api/           # API automation tests
│   ├── ui/            # Playwright UI tests
│   └── conftest.py    # Shared pytest fixtures
├── reports/           # Test reports
├── requirements.txt   # Python dependencies
└── pytest.ini       # Pytest configuration
```

## Running Tests

Run all tests:
```bash
pytest
```

Run API tests only:
```bash
pytest tests/api/
```

Run UI tests only:
```bash
pytest tests/ui/
```

Run UI tests with visible browser:
```bash
pytest tests/ui/ --headed
```

Run UI tests with debug slow-mo:
```bash
pytest tests/ui/ --headed --slowmo 1000
```

## Architecture Guidelines

- **API tests** should import from `utils.api_client` and `config.config`. Avoid using `requests` directly.
- **UI tests** should use Page Object Models from the `pages/` package instead of raw selectors in tests.
- **Test data** should live in `data/test_data.py` or loaded from environment variables via `.env`.
