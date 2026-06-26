# Project Memory: russia-tv-tests

## Overview

Production-ready test automation framework for [russia-tv.online](https://russia-tv.online/).

## Architecture

- **Framework**: Python 3.12 + pytest + Playwright (async) + httpx
- **Pattern**: Page Object Model + BaseAPI clients
- **Structure**:
  - `config/` — Settings, environments, browser configs
  - `core/` — BasePage, BaseAPI, BrowserManager, exceptions
  - `pages/` — Page Objects (HomePage, SchedulePage, ChannelPage, CategoryPage, Navigation)
  - `api/` — API clients (ChannelAPI, ScheduleAPI, SearchAPI)
  - `tests/` — unit / integration / e2e
  - `utils/` — date_helpers, screenshot_utils

## Key Design Decisions

1. **Async first**: All browser and API interactions use `async/await` for performance
2. **Pydantic settings**: Environment-based config via `.env` file
3. **Markers**: `unit`, `integration`, `e2e`, `smoke`, `slow`, `cross_browser`, `responsive`
4. **Allure**: Results written to `reports/allure-results/`
5. **CI/CD**: GitHub Actions with matrix testing (Chromium + Firefox)

## Site Analysis (russia-tv.online)

- **Stack**: Nuxt.js SPA, Tailwind CSS, SSR
- **No public REST API**: Site uses SSR; integration tests marked `xfail` for direct API calls
- **Selectors verified**:
  - Channel cards: `a[href*='region=']`
  - Search input: `input[placeholder*='название телеканала']`
  - Schedule link: `a[href='/epg']`

## Known Issues

- Integration tests use `xfail` because site lacks public REST API endpoints
- Error handling: now implemented in `BaseAPI` via `core/exceptions.py`

## Commands

```bash
# Linters
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run bandit -r api/ core/ pages/ utils/ config/

# Tests
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
uv run pytest tests/e2e/ -v

# Allure report
uv run allure serve reports/allure-results
```
