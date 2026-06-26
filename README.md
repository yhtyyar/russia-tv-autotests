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
- **CI/CD**: GitHub Actions (triggered manually by push/PR only)

## Architecture

```
russia-tv-tests/
├── config/          # Environment configs, browser launch args, Pydantic settings
├── core/            # BasePage, BaseAPI, BrowserManager, custom exceptions
├── pages/           # Page Objects + components (Home, Schedule, Channel, Category, Navigation)
├── api/             # Async API clients (Channel, Schedule, Search)
├── tests/
│   ├── smoke/       # Fast critical-path validation (< 2 min)
│   ├── unit/        # Fast isolated tests (date helpers, utilities, exceptions)
│   ├── integration/ # HTTP contract & site availability tests
│   └── e2e/         # Browser critical paths, responsive design, visual regression
├── utils/           # Screenshot capture, date formatting, image diff
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
7. **CI/CD on demand**: No nightly cron — runs only on push/PR to save GitHub Actions minutes

## Test Suite Analysis

| Suite | Files | Tests | Duration | Purpose |
|-------|-------|-------|----------|---------|
| **Smoke** | 1 | 4 | ~30s | Critical paths: site 200, channels load, schedule loads, search visible |
| **Unit** | 2 | 18 | < 1s | Pure logic: date helpers, exception hierarchy |
| **Integration** | 5 | 15 | ~10s | HTTP contracts: site availability (4 passed), API endpoints (11 xfail) |
| **E2E** | 4 | 11 | ~60s | Browser automation: home, schedule, filtering, responsive, visual regression |

**Total**: 33 tests executed (22 pass, 11 xfail expected due to SSR architecture).

### Markers

- `@pytest.mark.smoke` — Fast sanity check before deeper regression
- `@pytest.mark.unit` — Isolated logic tests
- `@pytest.mark.integration` — HTTP/API tests
- `@pytest.mark.e2e` — Browser automation tests
- `@pytest.mark.visual` — Screenshot comparison (requires baselines)
- `@pytest.mark.responsive` — Mobile/tablet viewport tests
- `@pytest.mark.slow` — Tests > 30 seconds

## Setup

```bash
# Install dependencies and browsers
make install

# Or manually:
uv sync --extra dev
uv run playwright install

# Create environment file
cp .env.example .env
```

## Running Tests

All commands are available via `Makefile`:

```bash
# Quick sanity check — smoke tests only (< 2 min)
make smoke

# Unit tests (fastest feedback)
make unit

# Integration tests (HTTP contracts)
make integration

# E2E tests (browser automation)
make e2e

# Visual regression (requires baseline screenshots)
make visual

# Update visual baselines after intentional UI changes
make visual-update

# Full regression suite (unit + integration + e2e, no visual)
make regression

# Quick validation before commit (unit + integration)
make test

# With code coverage
make coverage
```

### Direct pytest commands

```bash
# Run only smoke tests
uv run pytest tests/smoke/ -v

# Run everything except slow tests
uv run pytest -m "not slow" -v

# Run specific marker combinations
uv run pytest -m "smoke or unit" -v

# Update visual regression baselines
uv run pytest tests/e2e/test_visual_regression.py -v --update-baselines
```

## Reporting

### Allure HTML Report

Generate a static HTML report (requires Allure CLI installed separately):

```bash
# Generate static HTML report
make allure-html

# Open interactive report in browser
make allure
```

Reports are written to:
- `reports/allure-results/` — raw test result data
- `reports/allure-report/` — generated HTML pages (after `make allure-html`)
- `reports/screenshots/` — screenshots captured during test execution

### Coverage Report

```bash
make coverage
# Opens: htmlcov/index.html
```

## CI/CD

`.github/workflows/ci.yml` runs **only on push/PR** (no nightly cron to save GitHub Actions minutes):

- **Lint job**: Ruff, MyPy, Bandit
- **Unit tests**: Fast feedback loop
- **Integration tests**: HTTP contract validation
- **E2E matrix**: Chromium + Firefox with artifact upload on failure

## Author

Kadyrov Yhtyyar — QA Automation Engineer
