# russia-tv-tests

Professional test automation framework for [russia-tv.online](https://russia-tv.online/) — a Nuxt.js SPA TV guide platform.

Built as a portfolio project demonstrating production-grade QA engineering practices: async architecture, Page Object Model, CI/CD with matrix testing, security scanning, and comprehensive reporting.

## Tech Stack

- **Language**: Python 3.12
- **Test Runner**: pytest + pytest-asyncio
- **Browser Automation**: Playwright (async)
- **HTTP Client**: httpx
- **Configuration**: Pydantic Settings
- **Reporting**: Allure + pytest-html
- **Linting**: Ruff, MyPy (strict), Bandit
- **CI/CD**: GitHub Actions

## Architecture

```
russia-tv-tests/
├── config/          # Environment configs, browser launch args, Pydantic settings
├── core/            # BasePage, BaseAPI, BrowserManager, custom exceptions
├── pages/           # Page Objects + components (Home, Schedule, Channel, Category, Navigation)
├── api/             # Async API clients (Channel, Schedule, Search)
├── tests/
│   ├── unit/        # Fast isolated tests (date helpers, utilities)
│   ├── integration/ # HTTP contract & site availability tests
│   └── e2e/         # Browser critical paths, responsive design
├── utils/           # Screenshot capture, date formatting
├── test_data/       # JSON test data
└── reports/         # Allure results, screenshots, HTML reports
```

## Key Design Decisions

1. **Async-first**: All browser and API interactions use `async/await` for performance
2. **Type Safety**: Full type annotations, MyPy strict mode enabled
3. **Error Handling**: Custom domain exceptions (`APIError`, `BrowserError`) with structured logging
4. **SOLID**: Each class has single responsibility; no God-classes
5. **Security**: Bandit SAST scanning in CI; no secrets in repository
6. **Observability**: Allure reporting with screenshots on failure

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
# Unit tests (fastest)
uv run pytest tests/unit/ -v

# Integration tests (HTTP contracts)
uv run pytest tests/integration/ -v

# E2E tests (browser automation)
uv run pytest tests/e2e/ -v

# Exclude slow tests
uv run pytest -m "not slow" -v

# With coverage
uv run pytest --cov=. --cov-report=html
```

## Reporting

Allure results: `reports/allure-results/`

```bash
uv run allure serve reports/allure-results
```

## CI/CD

`.github/workflows/ci.yml` runs on push/PR and nightly:

- **Lint job**: Ruff, MyPy, Bandit
- **Unit tests**: Fast feedback loop
- **Integration tests**: HTTP contract validation
- **E2E matrix**: Chromium + Firefox with artifact upload

## Author

Kadyrov Yhtyyar — QA Automation Engineer
