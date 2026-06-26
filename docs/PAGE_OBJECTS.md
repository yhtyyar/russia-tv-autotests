# Page Objects

## BasePage

`core/base_page.py`

Abstract base class providing:
- `goto()` — navigation
- `wait_for_load()` — load state waiting
- `is_element_visible()` — visibility check
- `click()`, `fill()`, `get_text()` — common interactions
- `take_screenshot()` — full-page screenshot

## HomePage

`pages/home_page.py`

- `expect_channels_loaded()` — wait for channel cards
- `get_visible_channels()` — list visible channels
- `get_categories()` — list category filters
- `select_category(name)` — click category button
- `search(query)` — enter search text
- `click_load_more()` — load more channels

## SchedulePage

`pages/schedule_page.py`

- `select_date(date_str)` — choose schedule date
- `get_programs()` — list program items
- `get_available_dates()` — list date options

## ChannelPage

`pages/channel_page.py`

- `open_channel(channel_id)` — navigate to channel
- `get_channel_name()` — get channel title
- `get_programs()` — list channel programs

## CategoryPage

`pages/category_page.py`

- `open_category(category)` — navigate to category
- `get_category_title()` — get category title
- `get_channel_count()` — count channels in grid

## Navigation

`pages/components/navigation.py`

- `go_home()` — click home link
- `go_schedule()` — click schedule link
- `open_categories()` — open categories dropdown
