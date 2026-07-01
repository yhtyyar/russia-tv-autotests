# russia-tv-tests

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-8.x-yellow?logo=pytest)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-async-green?logo=microsoftedge)](https://playwright.dev/python/)
[![Ruff](https://img.shields.io/badge/Ruff-linter%20%26%20formatter-261230?logo=ruff)](https://docs.astral.sh/ruff/)
[![MyPy](https://img.shields.io/badge/MyPy-strict-2A6DB8?logo=python)](https://mypy-lang.org/)
[![Bandit](https://img.shields.io/badge/Bandit-SAST-red?logo=bandit)](https://bandit.readthedocs.io/)
[![Allure](https://img.shields.io/badge/Allure-Report-orange?logo=allure)](https://docs.qameta.io/allure/)

</div>

---

Профессиональный фреймворк автоматизированного тестирования для [russia-tv.online](https://russia-tv.online/) — телепрограммы на Nuxt.js SPA.

**[Allure-отчётность](https://yhtyyar.github.io/russia-tv-autotests/allure/)** — тренды, скриншоты, история прогонов.  
**[Performance Dashboard](https://yhtyyar.github.io/russia-tv-autotests/perf/)** — Core Web Vitals, история метрик, отклонения.

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


| Категория                                  | Технология                                                                  |
| --------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Язык**                                        | Python 3.12                                                                           |
| **Тестовый раннер**                   | pytest + pytest-asyncio                                                               |
| **Браузерная автоматизация** | Playwright (async API)                                                                |
| **HTTP-клиент**                               | httpx                                                                                 |
| **Конфигурация**                        | Pydantic Settings                                                                     |
| **Отчётность**                            | Allure + pytest-html                                                                  |
| **Линтинг**                                  | Ruff, MyPy (strict), Bandit                                                           |
| **Мягкие проверки**                   | pytest-check                                                                          |
| **Доступность**                          | axe-core (локальный, npm)                                                    |
| **Mobile**                                          | Playwright device emulation (iPhone 14 Pro)                                           |
| **Региональный браузер**         | Яндекс Браузер (Chromium-based, автоопределение пути) |
| **CI/CD**                                           | GitHub Actions (только ручной запуск)                               |

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

1. **Async-first** — `async/await` для Playwright
2. **Type Safety** — TypedDict + MyPy strict
3. **Обработка ошибок** — кастомные исключения с логированием
4. **SOLID** — одна ответственность на класс
5. **Безопасность** — Bandit SAST в CI
6. **Наблюдаемость** — Allure + скриншоты + логи
7. **Стабильность** — explicit waits вместо фиксированных пауз
8. **CI/CD по требованию** — `workflow_dispatch`

---

## Анализ тестового набора


| Набор      | Файлы | Тесты | Длительность | Назначение                                       | Техника                                                                                                                  |
| --------------- | ---------- | ---------- | ------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Smoke**       | 1          | 4          | ~30 s                    | Критические пути                            | —                                                                                                                              |
| **Unit**        | 2          | 18         | < 1 s                    | Чистая логика                                  | —                                                                                                                              |
| **Integration** | 2          | 8          | ~10 s                    | Доступность сайта, performance budget      | Граничные значения                                                                                             |
| **E2E**         | 19         | 77         | ~120 s                   | Браузерная автоматизация, chaos-инжиниринг            | Эквивалентное разбиение, диаграмма состояний, предугадывание ошибок |
| **Mobile**      | 2          | 14         | ~90 s                    | Мобильный viewport, touch, SPA навигация | Попарное тестирование                                                                                       |

**Итого**: 121 тест.

---

## Применённые техники дизайна тестов

1. **Эквивалентное разбиение** — поисковый ввод (валидные, невалидные, XSS, Unicode)
2. **Анализ граничных значений** — performance budget (2.0 s / 2.5 s)
3. **Диаграмма состояний** — навигация Главная ↔ Расписание ↔ Канал
4. **Предугадывание ошибок** — 404, офлайн, медленная сеть 3G
5. **Попарное тестирование** — вьюпорты (375×667, 768×1024, 1920×1080)

---

## Маркеры


| Маркер                    | Назначение                             |
| ------------------------------- | ------------------------------------------------ |
| `@pytest.mark.smoke`            | Sanity-проверка                          |
| `@pytest.mark.unit`             | Изолированные тесты            |
| `@pytest.mark.integration`      | Интеграция                             |
| `@pytest.mark.e2e`              | Браузерная автоматизация  |
| `@pytest.mark.visual`           | Визуальная регрессия          |
| `@pytest.mark.responsive`       | Адаптивные вьюпорты            |
| `@pytest.mark.error_handling`   | 404, офлайн, невалидный ввод |
| `@pytest.mark.state_transition` | Навигационные потоки          |
| `@pytest.mark.performance`      | Performance budget                               |
| `@pytest.mark.accessibility`    | WCAG / клавиатура                      |
| `@pytest.mark.flaky`            | Нестабильные (retry)                 |
| `@pytest.mark.slow`             | > 30 секунд                                |
| `@pytest.mark.chaos`            | Chaos-инжиниринг (сбои сети/API)  |
| `@pytest.mark.cookie`           | Cookie-баннер                              |
| `@pytest.mark.seo`              | Meta-теги                                    |
| `@pytest.mark.footer`           | Футер                                       |
| `@pytest.mark.load_more`        | Пагинация                               |
| `@pytest.mark.empty_state`      | Пустые состояния                  |
| `@pytest.mark.mobile`           | Мобильный viewport (390×844)           |
| `@pytest.mark.yandex`           | Яндекс Браузер                      |

---

## Установка

```bash
git clone https://github.com/yhtyyar/russia-tv-autotests.git
cd russia-tv-autotests
make install
# Или вручную: uv sync --extra dev && uv run playwright install && npm ci
cp .env.example .env
```

---

## Запуск тестов

```bash
# Основные наборы
make smoke          # Sanity (< 2 мин)
make unit           # Изолированные тесты
make integration    # Доступность + performance
make e2e            # Браузерная автоматизация
make mobile         # iPhone 14 Pro viewport
make yandex         # Яндекс Браузер
make regression     # Всё, кроме визуала
make regression-flaky # С retry flaky

# Специализированные
make visual         # Визуальная регрессия
make visual-update  # Обновить baseline
make error          # Граничные случаи
make state          # Навигационные потоки
make perf           # Performance budget
make a11y           # Accessibility
make cookie         # Cookie-баннер
make seo            # Meta-теги
make footer         # Футер
make load-more      # Пагинация
make empty          # Пустые состояния
make keyboard       # Клавиатура
make channel        # Страница канала
make date-picker    # Выбор даты

# Утилиты
make e2e-trace      # С Playwright tracing
make coverage       # Покрытие кода
make allure-html    # Сгенерировать Allure HTML
make allure         # Открыть Allure в браузере
make test           # unit + integration (быстро)
```

### Прямые команды pytest

```bash
uv run pytest tests/smoke/ -v
uv run pytest -m "not slow" -v
uv run pytest -m "smoke or unit" -v
uv run pytest tests/e2e/ -v -m mobile
BROWSER=yandex uv run pytest tests/e2e/ -v -m "not mobile"
uv run pytest tests/e2e/test_visual_regression.py -v --update-baselines
uv run pytest -m chaos -v  # Chaos-инжиниринг (сбои сети/API)
```

> Известные ограничения фичей сайта (dark mode, date picker и т.д.) описаны
> в [CLAUDE.md](CLAUDE.md#известные-ограничения).

---

## Логирование

```bash
LOG_LEVEL=DEBUG uv run pytest tests/e2e/ -v
```


| Место         | Уровень | Пример                                 |
| ------------------ | -------------- | -------------------------------------------- |
| `BasePage.goto()`  | INFO           | `Navigating to https://russia-tv.online/...` |
| `BasePage.click()` | DEBUG          | `Clicking selector: footer a`                |
| `BasePage.fill()`  | DEBUG          | `Filling selector input[type='search']`      |

---

## Отчётность

### Локальные отчёты


| Путь                  | Содержимое                |
| ------------------------- | ----------------------------------- |
| `reports/allure-results/` | Сырые результаты     |
| `reports/allure-report/`  | HTML (после`make allure-html`) |
| `reports/screenshots/`    | Скриншоты                  |
| `reports/traces/`         | Playwright-трейсы             |

```bash
make allure-html    # Сгенерировать
make allure         # Открыть в браузере
make e2e-trace      # С Playwright tracing
make coverage       # htmlcov/index.html
```

### Allure на GitHub Pages

**`https://yhtyyar.github.io/russia-tv-autotests/allure/`**

Живой отчёт с трендами, скриншотами и историей прогонов. Обновляется автоматически после каждого CI-прогона.

### Performance Dashboard

**`https://yhtyyar.github.io/russia-tv-autotests/perf/`**

Core Web Vitals (LCP, CLS, FCP, TTFB) с историей прогонов, трендами и сравнением с бюджетом. Обновляется автоматически.

---

## CI/CD

Запуск: **Actions → Test Automation CI → Run workflow** (`workflow_dispatch`)


| Suite         | Что запускается                                                                |
| ------------- | -------------------------------------------------------------------------------------------- |
| `lint`        | Ruff + MyPy + Bandit                                                                         |
| `unit`        | Быстрый фидбек                                                                  |
| `integration` | Доступность сайта                                                            |
| `e2e`         | Браузерная автоматизация (Chromium / Firefox / WebKit / Яндекс) |
| `mobile`      | Мобильные тесты                                                                |
| `all`         | Всё последовательно                                                        |

**Артефакты**: `screenshots-*.zip`, `allure-results-*.zip`, `junit-*.xml`

---

## Автор

**Yhtyyar** — QA Automation Engineer
Email: [kadyrow1506@gmail.com](mailto:kadyrow1506@gmail.com)

---

<div align="center">

*Проект создан в учебных целях для демонстрации компетенций в автоматизации тестирования.*

</div>
