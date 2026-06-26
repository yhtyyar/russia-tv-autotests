.PHONY: install test lint format coverage clean e2e integration unit smoke visual regression allure allure-html

install:
	uv sync --extra dev
	uv run playwright install

lint:
	uv run ruff check .
	uv run mypy .
	uv run bandit -r api/ core/ pages/ utils/ config/

format:
	uv run ruff check . --fix
	uv run ruff format .

# Fast smoke tests (< 2 min)
smoke:
	uv run pytest tests/smoke/ -v

# Unit tests
unit:
	uv run pytest tests/unit/ -v

# Integration tests
integration:
	uv run pytest tests/integration/ -v

# E2E tests (browser automation)
e2e:
	uv run pytest tests/e2e/ -v

# Visual regression tests (requires baselines)
visual:
	uv run pytest tests/e2e/test_visual_regression.py -v

visual-update:
	uv run pytest tests/e2e/test_visual_regression.py -v --update-baselines

# Error handling and edge cases
error:
	uv run pytest tests/e2e/test_error_pages.py -v

# State-transition navigation tests
state:
	uv run pytest tests/e2e/test_state_navigation.py -v

# Performance budget tests
perf:
	uv run pytest tests/integration/test_performance_budget.py -v

# Accessibility (WCAG) tests
a11y:
	uv run pytest tests/e2e/test_accessibility.py -v

# Full regression suite (unit + integration + e2e, excluding visual)
regression:
	uv run pytest tests/unit/ tests/integration/ tests/e2e/ -v -m "not visual"

# Regression with flaky-test retry (rerun failed up to 2 times)
regression-flaky:
	uv run pytest tests/unit/ tests/integration/ tests/e2e/ -v -m "not visual" --reruns 2 --reruns-delay 1

# Quick validation before commit
test:
	uv run pytest tests/unit/ tests/integration/ -v

# E2E with Playwright tracing for failed tests
e2e-trace:
	uv run pytest tests/e2e/ -v --tracing

coverage:
	uv run pytest --cov=. --cov-report=html --cov-report=term tests/unit/ tests/integration/

# Generate Allure HTML report (requires allure CLI installed)
allure-html:
	allure generate reports/allure-results -o reports/allure-report --clean

# Open Allure report in browser (requires allure CLI installed)
allure:
	allure serve reports/allure-results

clean:
	rm -rf reports/allure-results/* reports/screenshots/actual/* reports/screenshots/diff/* reports/html-report/* .pytest_cache .mypy_cache htmlcov
