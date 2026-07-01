"""Test data factories using factory_boy.

Usage:
    from test_data.factories import SearchQueryFactory
    query = SearchQueryFactory()
    batch = SearchQueryFactory.build_batch(3)
"""

import factory


class SearchQueryFactory(factory.Factory):
    """Factory for search queries with edge cases."""

    class Meta:
        model = dict

    query = factory.Iterator(
        [
            "Первый",
            "Новости",
            "Мультфильмы",
            "Спорт",
            "Фильмы",
            "а",
            "",
            "!@#$",
            "<script>alert(1)</script>",
            "а" * 200,
            "'; DROP TABLE channels; --",
        ]
    )
    # Совпадает с логикой в search_queries.json: одиночный буквенный
    # символ тоже считается валидным запросом (граничное значение).
    should_have_results = factory.LazyAttribute(
        lambda obj: len(obj.query) >= 1 and obj.query[0].isalpha()
    )
    id = factory.LazyAttribute(lambda obj: obj.query[:20].replace(" ", "_"))
    category = "валидный"
    reason = "Типичный поисковый запрос"
