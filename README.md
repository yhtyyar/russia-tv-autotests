# russia-tv-tests

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-8.x-yellow?logo=pytest)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-async-green?logo=microsoftedge)](https://playwright.dev/python/)
[![Ruff](https://img.shields.io/badge/Ruff-linter%20%26%20formatter-261230?logo=ruff)](https://docs.astral.sh/ruff/)
[![MyPy](https://img.shields.io/badge/MyPy-strict-2A6DB8?logo=python)](https://mypy-lang.org/)
[![Bandit](https://img.shields.io/badge/Bandit-SAST-red?logo=bandit)](https://bandit.readthedocs.io/)
[![Allure](https://img.shields.io/badge/Allure-Report-orange?logo=allure)](https://docs.qameta.io/allure/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

</div>

---

Профессиональный фреймворк автоматизированного тестирования для [russia-tv.online](https://russia-tv.online/) — телепрограммы на Nuxt.js SPA.

Проект создан для демонстрации production-практик QA-инженерии: асинхронная архитектура, Page Object Model, CI/CD с матричным тестированием, security-сканирование и комплексная отчётность.

---

## Содержание

- [Технологический стек](#технологический-стек)
- [Архитектура](#архитектура)
- [Ключевые архитектурные решения](#ключевые-архитектурные-решения)
- [Анализ тестового набора](#анализ-тестового-набора)
- [Применённые техники дизайна тестов](#применённые-техники-дизайна-тестов)
- [Маркеры](#маркеры)
- [Установка](#установка)
- [Запуск тестов](#запуск-тестов)
- [Логирование](#логирование)
- [Отчётность](#отчётность)
- [CI/CD](#cicd)
- [Автор](#автор)

---

## Технологический стек

| Категория | Технология |
|-----------|------------|
| **Язык** | Python 3.12 |
| **Тестовый раннер** | pytest + pytest-asyncio |
| **Браузерная автоматизация** | Playwright (async API) |
| **HTTP-клиент** | httpx |
| **Конфигурация** | Pydantic Settings |
| **Отчётность** | Allure + pytest-html |
| **Линтинг** | Ruff, MyPy (strict), Bandit |
| **Мягкие проверки** | pytest-check |
| **Доступность** | axe-core (локальный, npm) |
| **Mobile** | Playwright device emulation (iPhone 14 Pro) |
| **Региональный браузер** | Яндекс Браузер (Chromium-based, автоопределение пути) |
| **CI/CD** | GitHub Actions (только ручной запуск) |

---

## Архитектура

```
russia-tv-tests/
├── config/          # Конфиги окружения, аргументы запуска браузера, Pydantic settings
├── core/            # BasePage, BrowserManager, Logger, кастомные исключения
├── pages/           # Page Objects + компоненты (Home, Schedule, Channel, Category, Navigation)
├── tests/
│   ├── smoke/       # Быстрая проверка критических путей (< 2 мин)
│   ├── unit/        # Изолированные тесты (дата-хелперы, утилиты, исключения)
│   ├── integration/ # Доступность сайта и performance budget
│   └── e2e/         # Браузерные тесты: UX, SEO, a11y, тёмная тема, клавиатура
├── utils/           # Скриншоты, форматирование дат, сравнение изображений
├── test_data/       # JSON тестовые данные
└── reports/         # Allure-результаты, скриншоты, HTML-отчёты, JUnit XML
```

---

## Ключевые архитектурные решения

1. **Async-first**: Все взаимодействия с браузером через `async/await` для производительности и корректной работы с Playwright
2. **Type Safety**: Полная типизация с TypedDict, MyPy strict mode, отсутствие `Any` в публичных API
3. **Обработка ошибок**: Кастомные доменные исключения (`BrowserError`, `FrameworkError`) со структурированным логированием
4. **SOLID**: У каждого класса одна ответственность; нет God-классов
5. **Безопасность**: Bandit SAST-сканирование в CI; секретов в репозитории нет
6. **Наблюдаемость**: Allure-отчёты со скриншотами при падении + INFO/DEBUG логи во всех Page Objects
7. **Стабильность**: Все `wait_for_timeout` заменены на explicit waits (`wait_for_load_state`, `wait_for_selector`, `wait_for_function`)
8. **CI/CD по требованию**: Ручной запуск через `workflow_dispatch` для экономии GitHub Actions минут

---

## Анализ тестового набора

| Набор | Файлы | Тесты | Длительность | Назначение | Техника |
|-------|-------|-------|--------------|------------|---------|
| **Smoke** | 1 | 4 | ~30 s | Критические пути | — |
| **Unit** | 2 | 18 | < 1 s | Чистая логика | — |
| **Integration** | 2 | 7 | ~10 s | Доступность сайта, performance budget | Граничные значения |
| **E2E** | 15 | 55+ | ~120 s | Браузерная автоматизация, UX, SEO, a11y | Эквивалентное разбиение, диаграмма состояний, предугадывание ошибок |
| **Mobile** | 1 | 5 | ~30 s | Мобильный viewport, touch, адаптивность | Попарное тестирование |

**Итого**: 85+ тестов, покрывающих только внешние пользовательские сценарии.

---

## Применённые техники дизайна тестов

1. **Эквивалентное разбиение** — Поисковый ввод разделён на валидные/невалидные классы (пустой, 1 символ, нормальный, XSS, SQL injection, спецсимволы, Unicode)
2. **Анализ граничных значений** — Performance budget (пороги 2.0 s / 2.5 s), лимиты времени ответа
3. **Тестирование диаграммы состояний** — Навигация: Главная ↔ Расписание ↔ Карточка канала с возвратом и перезагрузкой
4. **Предугадывание ошибок** — 404-страницы, невалидные URL-параметры, офлайн-режим, медленная сеть 3G
5. **Попарное тестирование** — Адаптивные вьюпорты (мобильный 375×667, планшет 768×1024, десктоп 1920×1080)

---

## Маркеры

| Маркер | Назначение |
|--------|------------|
| `@pytest.mark.smoke` | Быстрая sanity-проверка перед глубокой регрессией |
| `@pytest.mark.unit` | Изолированные тесты логики |
| `@pytest.mark.integration` | Интеграционные тесты |
| `@pytest.mark.e2e` | Браузерная автоматизация |
| `@pytest.mark.visual` | Сравнение скриншотов (требуются базовые) |
| `@pytest.mark.responsive` | Тесты на мобильные/планшетные вьюпорты |
| `@pytest.mark.error_handling` | 404, офлайн, невалидный ввод |
| `@pytest.mark.state_transition` | Тесты навигационных потоков |
| `@pytest.mark.performance` | Бюджеты времени загрузки страниц |
| `@pytest.mark.accessibility` | WCAG / фокус с клавиатуры |
| `@pytest.mark.flaky` | Известные нестабильные тесты (retry включён) |
| `@pytest.mark.slow` | Тесты > 30 секунд |
| `@pytest.mark.dark_mode` | Тесты переключения темы |
| `@pytest.mark.cookie` | Тесты cookie-баннера |
| `@pytest.mark.seo` | Тесты meta-тегов и SEO |
| `@pytest.mark.footer` | Тесты ссылок в футере |
| `@pytest.mark.load_more` | Тесты пагинации / «Показать ещё» |
| `@pytest.mark.empty_state` | Тесты пустых состояний |
| `@pytest.mark.mobile` | Мобильный viewport (iPhone 14 Pro, 390×844) |
| `@pytest.mark.yandex` | Тесты специфичные для Яндекс Браузера |

---

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/yhtyyar/russia-tv-autotests.git
cd russia-tv-autotests

# Установка зависимостей и браузеров
make install

# Или вручную:
uv sync --extra dev
uv run playwright install
npm ci                # локальный axe-core для accessibility-тестов

# (Опционально) Установить Яндекс Браузер для E2E-тестов в нём:
# Linux:  sudo snap install yandex-browser
# macOS:  brew install --cask yandex
# Windows: choco install yandex-browser

# Создать файл окружения
cp .env.example .env
```

---

## Запуск тестов

Все команды доступны через `Makefile`:

```bash
# Быстрая sanity-проверка — только smoke (< 2 мин)
make smoke

# Unit-тесты (самый быстрый фидбек)
make unit

# Интеграционные тесты
make integration

# E2E-тесты (браузерная автоматизация)
make e2e

# Визуальная регрессия (требуются базовые скриншоты)
make visual

# Обновить базовые скриншоты после запланированных изменений UI
make visual-update

# Полная регрессия (unit + integration + e2e, без визуала)
make regression

# Регрессия с автоматическим retry нестабильных тестов
make regression-flaky

# Обработка ошибок и граничные случаи
make error

# Тесты навигационных потоков
make state

# Тесты performance budget
make perf

# Accessibility (WCAG) тесты
make a11y

# Тесты тёмной темы
make dark

# Тесты cookie-баннера
make cookie

# Тесты SEO и meta-тегов
make seo

# Тесты футера и навигации
make footer

# Тесты «Показать ещё» / пагинации
make load-more

# Тесты пустых состояний
make empty

# Тесты клавиатурной навигации
make keyboard

# Тесты страницы канала
make channel

# Тесты выбора даты
make date-picker

# E2E с Playwright tracing для упавших тестов
make e2e-trace

# Mobile E2E-тесты (iPhone 14 Pro viewport, touch-events)
make mobile

# E2E в Яндекс Браузере (требуется установленный Yandex Browser)
make yandex

# Быстрая проверка перед коммитом (unit + integration)
make test

# С покрытием кода
make coverage
```

### Прямые команды pytest

```bash
# Только smoke
uv run pytest tests/smoke/ -v

# Всё, кроме медленных
uv run pytest -m "not slow" -v

# Конкретные маркеры
uv run pytest -m "smoke or unit" -v

# Обновить базовые скриншоты визуальной регрессии
uv run pytest tests/e2e/test_visual_regression.py -v --update-baselines

# Mobile тесты
uv run pytest tests/e2e/ -v -m mobile

# E2E в Яндекс Браузере
BROWSER=yandex uv run pytest tests/e2e/ -v -m "not mobile"
```

---

## Логирование

Фреймворк использует стандартный модуль `logging` с префиксом `russia_tv_tests`.

- **Уровень по умолчанию**: `INFO`
- **Переменная окружения**: `LOG_LEVEL` (DEBUG, INFO, WARNING, ERROR)

```bash
LOG_LEVEL=DEBUG uv run pytest tests/e2e/ -v
```

### Что логируется

| Место | Уровень | Сообщение |
|-------|---------|-----------|
| `BasePage.goto()` | INFO | `Navigating to https://russia-tv.online/...` |
| `BasePage.goto()` | INFO | `Loaded https://russia-tv.online/...` |
| `BasePage.click()` | DEBUG | `Clicking selector: footer a` |
| `BasePage.fill()` | DEBUG | `Filling selector input[type='search']` |

---

## Отчётность

### Allure HTML Report

Генерация статического HTML-отчёта (требуется установленный Allure CLI):

```bash
# Сгенерировать статический HTML
make allure-html

# Открыть интерактивный отчёт в браузере
make allure
```

Отчёты пишутся в:

| Путь | Содержимое |
|------|------------|
| `reports/allure-results/` | Сырые результаты тестов |
| `reports/allure-report/` | Сгенерированные HTML-страницы (после `make allure-html`) |
| `reports/screenshots/` | Скриншоты, сделанные во время выполнения |
| `reports/traces/` | Playwright-трейсы упавших тестов (при `--tracing`) |

### Playwright Tracing

Для отладки упавших E2E-тестов записываются полные Playwright-трейсы:

```bash
# E2E с tracing (сохраняет .zip для каждого упавшего теста)
make e2e-trace

# Трейсы сохраняются в reports/traces/<test_name>.zip
# Открыть: npx playwright show-trace reports/traces/<name>.zip
```

### Отчёт о покрытии

```bash
make coverage
# Откроет: htmlcov/index.html
```

---

## CI/CD

CI/CD настроен **исключительно для ручного запуска** (`workflow_dispatch`) для экономии GitHub Actions минут.

### Запуск CI из GitHub

1. Перейти в **Actions** → **Test Automation CI**
2. Нажать **Run workflow**
3. Выбрать набор тестов:
   - `lint` — Ruff + MyPy + Bandit
   - `unit` — Быстрый фидбек
   - `integration` — Валидация доступности сайта
   - `e2e` — Браузерная автоматизация (Chromium / Firefox / WebKit / **Яндекс**)
   - `mobile` — Мобильные тесты (iPhone 14 Pro viewport)
   - `all` — Всё последовательно

### Артефакты CI

При падении автоматически загружаются:

- `screenshots-<browser>.zip` — скриншоты упавших тестов
- `screenshots-mobile.zip` — скриншоты mobile-тестов
- `allure-results-<browser>.zip` — сырые данные для Allure
- `junit-*.xml` — JUnit-compatible отчёты для интеграции с dashboards

---

## Автор

**Yhtyyar** — QA Automation Engineer  
Email: [kadyrow1506@gmail.com](mailto:kadyrow1506@gmail.com)

---

<div align="center">

*Проект создан в учебных целях для демонстрации компетенций в автоматизации тестирования.*

</div>
