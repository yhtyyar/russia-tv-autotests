# Project Memory: russia-tv-tests

## Overview

Production-ready test automation framework for [russia-tv.online](https://russia-tv.online/).

## Architecture

- **Framework**: Python 3.12 + pytest + Playwright (async) + httpx
- **Pattern**: Page Object Model (общая логика — в `core/base_page.py`)
- **Structure**:
  - `config/` — Settings, environments, browser configs
  - `core/` — BasePage, BrowserManager, self-healing локаторы, exceptions
  - `pages/` — Page Objects (HomePage, SchedulePage, ChannelPage, CategoryPage, Navigation)
  - `tests/` — unit / integration / e2e
  - `utils/` — date_helpers, screenshot_utils
  - `test_data/` — фикстуры (`search_queries.json`) и `factories.py` (SearchQueryFactory)

  Отдельного слоя API-клиентов (`api/`, `BaseAPI`) в проекте больше нет —
  он был удалён как мёртвый код, поскольку у сайта нет публичного REST API
  (см. «Site Analysis» ниже). Интеграционные тесты обращаются к сайту напрямую
  через `httpx.AsyncClient`.

## Key Design Decisions

1. **Async first**: All browser and API interactions use `async/await` for performance
2. **Pydantic settings**: Environment-based config via `.env` file
3. **Markers**: `unit`, `integration`, `e2e`, `smoke`, `slow`, `cross_browser`, `responsive`, `chaos`
4. **Allure**: Results written to `reports/allure-results/`
5. **CI/CD**: GitHub Actions with matrix testing (Chromium + Firefox)

## Site Analysis (russia-tv.online)

- **Stack**: Nuxt.js SPA, Tailwind CSS, SSR
- **No public REST API**: Site uses SSR; integration tests hit the site directly via httpx
- **Реальная схема URL канала**: `/{slug}?region={region_id}` (например,
  `/1kanal?region=21`), НЕ `/channel/{id}`
- **Селекторы, проверенные на живом сайте (2026-07-01)**:
  - Карточки каналов: `a[href*='region=']`
  - Поле поиска: `input[placeholder*='название телеканала']`
  - Ссылка на расписание: `a[href='/epg']`
  - Название канала на странице канала: `h1[data-test='current-channel-name']`
  - Программа канала (EPG): `[data-test='epg-program-start']` / `[data-test='epg-program-title']`
  - Кнопки жанровых категорий на главной: `li[data-test='category-button']`
    (Популярное, Все, Эфирные, Фильмы, Детям, Музыка, Развлечения, Познавательные, Спорт, Новости, Местные)
  - Индикатор «ничего не найдено» при поиске: `[data-test='channel-search-empty']`
  - Cookie-баннер: `[data-test='cookie-description']`, кнопка принятия — `button[data-test='cookie-agree-button']`

## Известные ограничения

- **Тёмная тема (dark mode) отсутствует на сайте.** Полная проверка DOM
  (главная, мобильная версия, страница канала) не нашла ни одного элемента
  с `aria-label`/`data-testid`, указывающего на переключатель темы.
  `tests/e2e/test_dark_mode.py` удалён, соответствующие методы убраны из
  Page Objects.
- **Date picker отсутствует** на `/epg` и на странице конкретного канала —
  ни нативного `<input type="date">`, ни кастомного `<select>`-виджета
  нет. `SchedulePage.select_date()` поднимает `NotImplementedError` в этом
  случае; тесты в `test_date_picker.py` корректно пропускаются (`skip`), а не
  притворяются пройденными.
  Отдельно на странице **конкретного канала** (`/{slug}?region=...`) есть
  переключение дня EPG через кнопки `button[data-test^="epg-DD.MM.YYYY"]`
  (например, `epg-01.07.2026`) — это не тот же механизм, что «date picker»
  на агрегированной странице расписания, и пока не покрыт тестами.
- **Фильтрация каналов по категориям работает** (жанровые категории —
  реальная фича сайта, см. «Site Analysis» выше) — ранее
  `HomePage.get_categories()` возвращал захардкоженную заглушку вместо
  реального DOM; это исправлено.

## Commands

```bash
# Linters
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run bandit -r core/ pages/ utils/ config/

# Tests
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
uv run pytest tests/e2e/ -v

# Allure report
uv run allure serve reports/allure-results
```
