# Changelog

Все значимые изменения в проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),  
а версионирование следует [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Added

- CI/CD workflow только для ручного запуска (`workflow_dispatch`) с выбором suite и browser
- JUnit XML артефакты в CI
- CODEOWNERS, Dependabot, Issue/PR templates
- Цель `make pre-commit` в Makefile
- Раздел «Логирование» в README
- Badges (shields) в README
- Оглавление (TOC) в README

### Changed

- README переписан в профессиональном стиле с таблицами и чёткой структурой
- `.pre-commit-config.yaml`: удалена несуществующая папка `api/`

### Fixed

- Зарегистрирован pytest-маркер `chaos`; `pytest_collection_modifyitems` больше
  не вызывает `allure.dynamic.*` на этапе collection (перенесено в autouse-фикстуру)
  — `uv run pytest` больше не падает с `INTERNALERROR`
- `HomePage.get_categories()` теперь парсит реальный DOM (жанровые категории,
  `li[data-test='category-button']`) вместо возврата захардкоженной заглушки
- `SchedulePage.select_date()` переписан для нативного `input[type="date"]`
  с явным `NotImplementedError`, если date picker отсутствует на странице
- `ChannelPage` переведён на реальную схему URL сайта — `/{slug}?region={id}`
  вместо несуществующей `/channel/{id}`
- Исправлен системный баг с CSS-селекторами через запятую в
  `pages/category_page.py`, `pages/channel_page.py`
- Исправлен баг в `core/self_healing.py`: `RoleFallback` подставлял `role=link`
  почти для любого селектора (проверка на подстроку `"a" in selector`)
- Заменены слабые/тавтологические утверждения (`assert X is not None` для
  методов, никогда не возвращающих `None`; сравнение URL) на осмысленные
  проверки реального состояния DOM — `test_channel_filtering.py`,
  `test_chaos_resilience.py`, `test_error_pages.py`, `test_state_navigation.py`,
  `test_empty_states.py`, `test_search_edge_cases.py`
- Все `page.wait_for_timeout(N)` заменены на `expect(...).to_be_visible()` /
  `wait_for_selector` / `wait_for_url`, кроме документированного случая в
  `test_mobile_home.py` (networkidle не наступает из-за фоновых метрик/рекламы)
- Устранена тройная дублирование dark-mode/cookie/footer/meta-tags методов
  между `HomePage`, `ChannelPage`, `SchedulePage` — общая логика перенесена
  в `core/base_page.py`
- Все `wait_for_timeout` в тестах e2e заменены на explicit waits
- Удалён мёртвый код API (`api_base_url`, `api_timeout`, `test_data_loader.py`)
- Bare `pass` в тестах заменён на `pytest.skip`
- Исправлено поле автора во всех git-коммитах на `Yhtyyar <kadyrow1506@gmail.com>`

### Removed

- `tests/e2e/test_dark_mode.py` и все связанные методы/селекторы — на живом
  сайте нет переключателя тёмной темы (проверено вручную)
- Неиспользуемые `ChannelFactory`, `CategoryFactory`, `ScheduleItemFactory` из
  `test_data/factories.py` (осталась только `SearchQueryFactory`)
- `test_data/channels.json` — не использовался ни одним тестом
- Зависимость `faker` из dev-extras (была нужна только удалённой `ScheduleItemFactory`)

## [1.0.0] — 2026-06-29

### Added

- Профессиональный фреймворк автоматизации тестирования для russia-tv.online
- 80+ тестов: smoke, unit, integration, e2e
- Page Object Model с TypedDict типизацией
- Playwright async API для браузерной автоматизации
- Allure + pytest-html отчётность
- Локальный axe-core для accessibility-тестов
- Мягкие проверки через pytest-check
- Логирование во всех Page Objects
- GitHub Actions CI с матричным тестированием (Chromium + Firefox)
- Visual regression через Pillow
- Playwright tracing для отладки упавших тестов
