"""Environment-specific URL configurations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Environment:
    """Environment configuration."""

    name: str
    base_url: str
    api_base_url: str


ENVIRONMENTS = {
    "dev": Environment(
        name="dev",
        base_url="https://dev.russia-tv.online/",
        api_base_url="https://dev.russia-tv.online/api",
    ),
    "staging": Environment(
        name="staging",
        base_url="https://staging.russia-tv.online/",
        api_base_url="https://staging.russia-tv.online/api",
    ),
    "prod": Environment(
        name="prod",
        base_url="https://russia-tv.online/",
        api_base_url="https://russia-tv.online/api",
    ),
}


def get_environment(name: str) -> Environment:
    """Return environment configuration by name.

    Args:
        name: Environment name (dev, staging, prod).

    Returns:
        Environment configuration.

    Raises:
        ValueError: If environment name is unknown.
    """
    if name not in ENVIRONMENTS:
        msg = f"Unknown environment: {name}. Available: {list(ENVIRONMENTS.keys())}"
        raise ValueError(msg)
    return ENVIRONMENTS[name]
