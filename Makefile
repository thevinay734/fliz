.PHONY: test test-ui test-api install

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
