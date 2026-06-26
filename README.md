# russia-tv-tests

Production-ready test automation framework for [russia-tv.online](https://russia-tv.online/).

## Structure

```
russia-tv-tests/
├── config/          # Settings, environments, browsers
├── core/            # Base classes (Page Object, API, BrowserManager)
├── pages/           # Page Objects + components
├── api/             # API clients
├── tests/
│   ├── unit/        # Fast unit tests
│   ├── integration/ # API integration tests
│   └── e2e/         # Browser end-to-end tests
├── utils/           # Helpers (dates, screenshots, reporting)
├── test_data/       # JSON test data
└── reports/         # Allure + HTML reports
```

## Setup

```bash
# Install dependencies
uv sync --extra dev

# Install Playwright browsers
uv run playwright install

# Create environment file
cp .env.example .env
```

## Running Tests

```bash
# Unit tests
uv run pytest tests/unit/ -v

# Integration tests
uv run pytest tests/integration/ -v

# E2E tests
uv run pytest tests/e2e/ -v

# All tests with markers
uv run pytest -m "not slow" -v
```

## Reporting

Allure results are written to `reports/allure-results/`.
Generate and open the report:

```bash
uv run allure serve reports/allure-results
```

## CI/CD

GitHub Actions workflows in `.github/workflows/ci.yml` run on:
- Push to `main` or `develop`
- Pull requests to `main`
- Nightly schedule at 02:00 UTC
