.PHONY: install test lint format coverage clean e2e integration unit

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

unit:
	uv run pytest tests/unit/ -v

integration:
	uv run pytest tests/integration/ -v

e2e:
	uv run pytest tests/e2e/ -v

test:
	uv run pytest tests/unit/ tests/integration/ -v

coverage:
	uv run pytest --cov=. --cov-report=html --cov-report=term tests/unit/ tests/integration/

allure:
	uv run allure serve reports/allure-results

clean:
	rm -rf reports/allure-results/* reports/screenshots/* reports/html-report/* .pytest_cache .mypy_cache htmlcov
