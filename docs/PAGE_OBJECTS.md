# Page Objects

## BasePage

`core/base_page.py`

Абстрактный базовый класс, предоставляющий:
- `goto()` — навигация с retry при сетевых ошибках
- `wait_for_load()` — ожидание состояния загрузки
- `is_element_visible()` — проверка видимости
- `click()`, `fill()`, `get_text()` — общие взаимодействия
- `take_screenshot()` — скриншот всей страницы

## HomePage

`pages/home_page.py`

- `expect_channels_loaded()` — ожидание загрузки карточек каналов
- `get_visible_channels()` — список видимых каналов
- `get_visible_categories()` — список категорий из DOM
- `select_category(name)` — клик по кнопке категории
- `search(query)` — ввод поискового запроса
- `click_load_more()` — загрузить больше каналов
- `is_dark_mode_toggle_visible()` — проверить наличие переключателя темы
- `toggle_dark_mode()` — клик по переключателю темы
- `is_dark_mode_active()` — проверить, включена ли тёмная тема
- `is_cookie_banner_visible()` — проверить cookie-баннер
- `accept_cookies()` — закрыть cookie-баннер
- `is_footer_visible()` — проверить наличие футера
- `get_footer_links()` — список ссылок футера с текстом и href
- `is_empty_state_visible()` — проверить состояние «нет результатов»
- `get_meta_tags()` — извлечь SEO meta-теги

## SchedulePage

`pages/schedule_page.py`

- `select_date(date_str)` — выбрать дату в расписании
- `get_channel_links()` — список ссылок каналов
- `get_programs()` — список передач с названием и временем
- `get_available_dates()` — список доступных дат
- `is_empty_schedule_visible()` — проверить пустое расписание
- `toggle_dark_mode()` — клик по переключателю темы
- `is_dark_mode_active()` — проверить состояние тёмной темы
- `get_meta_tags()` — извлечь SEO meta-теги

## ChannelPage

`pages/channel_page.py`

- `open_channel(channel_id)` — открыть страницу канала
- `get_channel_name()` — получить название канала
- `get_programs()` — список передач канала
- `is_current_program_visible()` — проверить индикатор текущей передачи
- `toggle_dark_mode()` — клик по переключателю темы
- `is_dark_mode_active()` — проверить состояние тёмной темы
- `is_footer_visible()` — проверить наличие футера
- `is_cookie_banner_visible()` — проверить cookie-баннер
- `accept_cookies()` — закрыть cookie-баннер
- `get_meta_tags()` — извлечь SEO meta-теги

## CategoryPage

`pages/category_page.py`

- `open_category(category)` — открыть страницу категории
- `get_category_title()` — получить название категории
- `get_channel_count()` — посчитать каналы в сетке

## Navigation

`pages/components/navigation.py`

- `go_home()` — клик по ссылке на главную
- `go_schedule()` — клик по ссылке на расписание
- `open_categories()` — открыть выпадающий список категорий
