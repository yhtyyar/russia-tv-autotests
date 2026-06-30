"""Test data factories using factory_boy + Faker.

Usage:
    from test_data.factories import ChannelFactory, CategoryFactory
    channel = ChannelFactory(name="Первый канал")
    random_channels = ChannelFactory.build_batch(5)
"""

import factory
from faker import Faker

faker = Faker("ru_RU")


class CategoryFactory(factory.Factory):
    """Factory for channel categories."""

    class Meta:
        model = dict

    id = factory.Sequence(lambda n: f"cat_{n}")
    name = factory.Iterator([
        "Эфирные", "Фильмы", "Детям", "Музыка", "Новости",
        "Спорт", "Познавательные", "Развлечения",
    ])
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(" ", "_"))


class ChannelFactory(factory.Factory):
    """Factory for TV channels."""

    class Meta:
        model = dict

    id = factory.Sequence(lambda n: str(n))
    name = factory.Iterator([
        "Первый канал", "Россия 1", "НТВ", "ТНТ", "СТС",
        "Карусель", "Мульт", "Муз-ТВ", "РЕН ТВ", "ТВ-3",
        "Пятница!", "Домашний", "ТВ Центр", "Россия 24",
    ])
    category = factory.SubFactory(CategoryFactory)
    logo_url = factory.LazyAttribute(
        lambda obj: f"/logos/{obj.name.lower().replace(' ', '_').replace('!', '')}.png"
    )
    description = factory.LazyAttribute(
        lambda obj: f"Телеканал {obj.name} — лучшие программы"
    )


class SearchQueryFactory(factory.Factory):
    """Factory for search queries with edge cases."""

    class Meta:
        model = dict

    query = factory.Iterator([
        "Первый", "Новости", "Мультфильмы", "Спорт", "Фильмы",
        "а", "", "!@#$", "<script>alert(1)</script>",
        "а" * 200, "'; DROP TABLE channels; --",
    ])
    should_have_results = factory.LazyAttribute(
        lambda obj: len(obj.query) > 1 and obj.query[0].isalpha()
    )
    id = factory.LazyAttribute(lambda obj: obj.query[:20].replace(" ", "_"))
    category = "валидный"
    reason = "Типичный поисковый запрос"


class ScheduleItemFactory(factory.Factory):
    """Factory for TV schedule items."""

    class Meta:
        model = dict

    channel_id = factory.Sequence(lambda n: str(n))
    channel_name = factory.Iterator([
        "Первый канал", "Россия 1", "НТВ", "ТНТ",
    ])
    program = factory.LazyAttribute(
        lambda obj: f"{faker.word().capitalize()} {faker.word()}"
    )
    start_time = factory.LazyAttribute(lambda _: faker.time(pattern="%H:%M"))
    duration_minutes = factory.Iterator([15, 30, 45, 60, 90, 120])
