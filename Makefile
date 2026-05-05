.PHONY: install test test-ui test-api run-login-flow docker-build docker-test docker-ui-test allure-report clean lint

# --- Local commands ---

install:
	.venv/bin/pip install -r requirements.txt
	.venv/bin/playwright install

test:
	.venv/bin/python -m pytest

test-ui:
	.venv/bin/python -m pytest tests/ui/ -m ui --headed

test-api:
	.venv/bin/python -m pytest tests/api/ -m api

run-login-flow:
	.venv/bin/python -m pytest tests/ui/test_login_full_flow.py --headed

lint:
	python3 -m py_compile core/*.py pages/*.py services/*.py factories/*.py utils/*.py tests/**/*.py

# --- Docker commands ---

docker-build:
	docker compose build

docker-test:
	docker compose up tests

docker-ui-test:
	docker compose up ui-tests

# --- Reporting ---

allure-report:
	allure serve reports/allure-results

# --- Cleanup ---

clean:
	rm -rf reports/allure-results/* logs/* __pycache__ .pytest_cache
