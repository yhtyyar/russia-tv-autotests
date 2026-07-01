.PHONY: install test lint format pre-commit changelog coverage clean e2e integration unit smoke visual regression regression-flaky error state perf a11y cookie seo footer load-more empty keyboard channel date-picker e2e-trace allure allure-html mobile yandex

install:
	uv sync --extra dev
	uv run playwright install

lint:
	uv run ruff check .
	uv run mypy .
	uv run bandit -r core/ pages/ utils/ config/

format:
	uv run ruff check . --fix
	uv run ruff format .

pre-commit:
	uv run pre-commit run --all-files

# Сгенерировать CHANGELOG из Conventional Commits
changelog:
	uv run git-cliff --output CHANGELOG.md

# Быстрые smoke-тесты (< 2 мин)
smoke:
	uv run pytest tests/smoke/ -v

# Unit-тесты
unit:
	uv run pytest tests/unit/ -v

# Интеграционные тесты
integration:
	uv run pytest tests/integration/ -v

# E2E-тесты (браузерная автоматизация)
e2e:
	uv run pytest tests/e2e/ -v

# Тесты визуальной регрессии (требуются базовые скриншоты)
visual:
	uv run pytest tests/e2e/test_visual_regression.py -v

visual-update:
	uv run pytest tests/e2e/test_visual_regression.py -v --update-baselines

# Обработка ошибок и граничные случаи
error:
	uv run pytest tests/e2e/test_error_pages.py -v

# Тесты навигационных потоков
state:
	uv run pytest tests/e2e/test_state_navigation.py -v

# Тесты performance budget
perf:
	uv run pytest tests/integration/test_performance_budget.py -v

# Accessibility (WCAG) тесты
a11y:
	uv run pytest tests/e2e/test_accessibility.py -v

# Тесты cookie-баннера
cookie:
	uv run pytest tests/e2e/test_cookie_consent.py -v

# Тесты SEO и meta-тегов
seo:
	uv run pytest tests/e2e/test_seo_meta.py -v

# Тесты футера и навигации
footer:
	uv run pytest tests/e2e/test_footer_links.py -v

# Тесты «Показать ещё» / пагинации
load-more:
	uv run pytest tests/e2e/test_load_more.py -v

# Тесты пустых состояний
empty:
	uv run pytest tests/e2e/test_empty_states.py -v

# Тесты клавиатурной навигации
keyboard:
	uv run pytest tests/e2e/test_keyboard_navigation.py -v

# Тесты страницы канала
channel:
	uv run pytest tests/e2e/test_channel_detail.py -v

# Тесты выбора даты
date-picker:
	uv run pytest tests/e2e/test_date_picker.py -v

# Полная регрессия (unit + integration + e2e, без визуала)
regression:
	uv run pytest tests/unit/ tests/integration/ tests/e2e/ -v -m "not visual"

# Регрессия с retry для нестабильных тестов (до 2 повторов)
regression-flaky:
	uv run pytest tests/unit/ tests/integration/ tests/e2e/ -v -m "not visual" --reruns 2 --reruns-delay 1

# Быстрая проверка перед коммитом
test:
	uv run pytest tests/unit/ tests/integration/ -v

# E2E с Playwright tracing для упавших тестов
e2e-trace:
	uv run pytest tests/e2e/ -v --tracing

# Mobile E2E-тесты (iPhone 14 Pro viewport)
mobile:
	uv run pytest tests/e2e/ -v -m mobile

# E2E в Яндекс Браузере (локально, требуется установленный Yandex Browser)
yandex:
	BROWSER=yandex uv run pytest tests/e2e/ -v -m "not mobile"

coverage:
	uv run pytest --cov=. --cov-report=html --cov-report=term tests/unit/ tests/integration/

# Сгенерировать Allure HTML-отчёт (требуется установленный allure CLI)
allure-html:
	allure generate reports/allure-results -o reports/allure-report --clean

# Открыть Allure-отчёт в браузере (требуется установленный allure CLI)
allure:
	allure serve reports/allure-results

clean:
	rm -rf reports/allure-results/* reports/screenshots/actual/* reports/screenshots/diff/* reports/html-report/* .pytest_cache .mypy_cache htmlcov
