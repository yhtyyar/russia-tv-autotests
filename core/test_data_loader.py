"""Test data loading utilities."""

import json
from pathlib import Path
from typing import Any, cast

TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"


def load_json(filename: str) -> dict[str, Any]:
    """Load JSON test data file.

    Args:
        filename: Name of JSON file in test_data directory.

    Returns:
        Parsed JSON content.

    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If file is not valid JSON.
    """
    path = TEST_DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        return cast("dict[str, Any]", json.load(f))


def save_json(filename: str, data: dict[str, Any]) -> None:
    """Save data to JSON test data file.

    Args:
        filename: Name of JSON file in test_data directory.
        data: Data to serialize.
    """
    path = TEST_DATA_DIR / filename
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
