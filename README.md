# russia-tv-tests

Профессиональный фреймворк автоматизированного тестирования для [russia-tv.online](https://russia-tv.online/) — телепрограммы на Nuxt.js SPA.

Проект создан для демонстрации production-практик QA-инженерии: асинхронная архитектура, Page Object Model, CI/CD с матричным тестированием, security-сканирование и комплексная отчётность.

## Технологический стек

- **Язык**: Python 3.12
- **Тестовый раннер**: pytest + pytest-asyncio
- **Браузерная автоматизация**: Playwright (async)
- **HTTP-клиент**: httpx
- **Конфигурация**: Pydantic Settings
- **Отчётность**: Allure + pytest-html
- **Линтинг**: Ruff, MyPy (strict), Bandit
- **CI/CD**: GitHub Actions (только по push/PR)

## Архитектура

```
russia-tv-tests/
├── config/          # Конфиги окружения, аргументы запуска браузера, Pydantic settings
├── core/            # BasePage, BrowserManager, кастомные исключения
├── pages/           # Page Objects + компоненты (Home, Schedule, Channel, Category, Navigation)
├── tests/
│   ├── smoke/       # Быстрая проверка критических путей (< 2 мин)
│   ├── unit/        # Изолированные тесты (дата-хелперы, утилиты, исключения)
│   ├── integration/ # Доступность сайта и performance budget
│   └── e2e/         # Браузерные тесты, адаптивность, визуальная регрессия, тёмная тема, SEO
├── utils/           # Скриншоты, форматирование дат, сравнение изображений
├── test_data/       # JSON тестовые данные
└── reports/         # Allure-результаты, скриншоты, HTML-отчёты
```

## Ключевые архитектурные решения

1. **Async-first**: Все взаимодействия с браузером через `async/await` для производительности
2. **Type Safety**: Полная типизация, MyPy strict mode включён
3. **Обработка ошибок**: Кастомные доменные исключения (`APIError`, `BrowserError`) со структурированным логированием
4. **SOLID**: У каждого класса одна ответственность; нет God-классов
5. **Безопасность**: Bandit SAST-сканирование в CI; секретов в репозитории нет
6. **Наблюдаемость**: Allure-отчёты со скриншотами при падении
7. **CI/CD по требованию**: Нет ночных запусков — только по push/PR для экономии GitHub Actions

## Анализ тестового набора

| Набор | Файлы | Тесты | Длительность | Назначение | Техника |
|-------|-------|-------|--------------|------------|---------|
| **Smoke** | 1 | 4 | ~30s | Критические пути | — |
| **Unit** | 2 | 18 | < 1s | Чистая логика | — |
| **Integration** | 2 | 7 | ~10s | Доступность сайта, performance budget | Граничные значения |
| **E2E** | 15 | 55+ | ~120s | Браузерная автоматизация, UX, SEO, a11y | Эквивалентное разбиение, диаграмма состояний, предугадывание ошибок |

**Итого**: 80+ тестов, покрывающих только внешние пользовательские сценарии.

### Применённые техники дизайна тестов

1. **Эквивалентное разбиение** — Поисковый ввод разделён на валидные/невалидные классы (пустой, 1 символ, нормальный, XSS, SQL injection, спецсимволы, Unicode)
2. **Анализ граничных значений** — Performance budget (пороги 2.0s/2.5s), лимиты времени ответа API
3. **Тестирование диаграммы состояний** — Навигация: Главная ↔ Расписание ↔ Карточка канала с возвратом и перезагрузкой
4. **Предугадывание ошибок** — 404-страницы, невалидные URL-параметры, офлайн-режим, медленная сеть 3G
5. **Попарное тестирование / Таблица решений** — Адаптивные вьюпорты (мобильный 375×667, планшет 768×1024, десктоп 1920×1080)

### Маркеры

- `@pytest.mark.smoke` — Быстрая sanity-проверка перед глубокой регрессией
- `@pytest.mark.unit` — Изолированные тесты логики
- `@pytest.mark.integration` — Интеграционные тесты
- `@pytest.mark.e2e` — Браузерная автоматизация
- `@pytest.mark.visual` — Сравнение скриншотов (требуются базовые)
- `@pytest.mark.responsive` — Тесты на мобильные/планшетные вьюпорты
- `@pytest.mark.error_handling` — 404, офлайн, невалидный ввод
- `@pytest.mark.state_transition` — Тесты навигационных потоков
- `@pytest.mark.performance` — Бюджеты времени загрузки страниц
- `@pytest.mark.accessibility` — WCAG / фокус с клавиатуры
- `@pytest.mark.flaky` — Известные нестабильные тесты (retry включён)
- `@pytest.mark.slow` — Тесты > 30 секунд
- `@pytest.mark.dark_mode` — Тесты переключения темы
- `@pytest.mark.cookie` — Тесты cookie-баннера
- `@pytest.mark.seo` — Тесты meta-тегов и SEO
- `@pytest.mark.footer` — Тесты ссылок в футере
- `@pytest.mark.load_more` — Тесты пагинации / «Показать ещё»
- `@pytest.mark.empty_state` — Тесты пустых состояний

## Установка

```bash
# Установка зависимостей и браузеров
make install

# Или вручную:
uv sync --extra dev
uv run playwright install

# Создать файл окружения
cp .env.example .env
```

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
```

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
- `reports/allure-results/` — сырые результаты тестов
- `reports/allure-report/` — сгенерированные HTML-страницы (после `make allure-html`)
- `reports/screenshots/` — скриншоты, сделанные во время выполнения

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

## CI/CD

`.github/workflows/ci.yml` запускается **только по push/PR** (нет ночных запусков для экономии GitHub Actions):

- **Lint**: Ruff, MyPy, Bandit
- **Unit tests**: Быстрый фидбек
- **Integration tests**: Валидация доступности сайта
- **E2E matrix**: Chromium + Firefox с загрузкой артефактов при падении

## Автор

**Yhtyyar** — QA Automation Engineer  
Email: kadyrow1506@gmail.com
