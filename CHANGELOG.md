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

- Все `wait_for_timeout` заменены на explicit waits
- Удалён мёртвый код API (`api_base_url`, `api_timeout`, `test_data_loader.py`)
- Bare `pass` в тестах заменён на `pytest.skip`
- Исправлено поле автора во всех git-коммитах на `Yhtyyar <kadyrow1506@gmail.com>`

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
