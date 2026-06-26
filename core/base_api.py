"""Base API client with common HTTP operations."""

import json
import logging
from typing import Any, cast

import httpx

from config.settings import get_settings
from core.exceptions import APIError

logger = logging.getLogger(__name__)


class BaseAPI:
    """Base API client with common HTTP operations and response validation."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        """Initialize API client.

        Args:
            client: Optional pre-configured httpx.AsyncClient.
        """
        self.settings = get_settings()
        self.base_url = self.settings.api_base_url.rstrip("/")
        self.timeout = self.settings.api_timeout
        self._client = client

    def _resolve_url(self, endpoint: str) -> str:
        """Build full URL from endpoint, ensuring base_url is prepended.

        Args:
            endpoint: Relative or absolute endpoint path.

        Returns:
            Full URL string.
        """
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        base = self.base_url.rstrip("/")
        path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{base}{path}"

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create httpx client.

        Returns:
            Configured AsyncClient instance.
        """
        if self._client is not None:
            return self._client
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Accept": "application/json", "User-Agent": "russia-tv-tests/0.1.0"},
        )

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Execute GET request.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.
            headers: Additional headers.

        Returns:
            HTTP response.

        Raises:
            APIError: On HTTP status errors or network failures.
        """
        client = self._get_client()
        url = self._resolve_url(endpoint) if self._client else endpoint
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            logger.exception(
                "API HTTP error: %s - %s", exc.response.status_code, exc.response.text
            )
            raise APIError(
                f"HTTP error {exc.response.status_code} for {url}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            logger.exception("API request error: %s", exc)
            raise APIError(f"Request error for {url}: {exc}") from exc

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Execute POST request.

        Args:
            endpoint: API endpoint path.
            data: Form data.
            json_data: JSON payload.
            headers: Additional headers.

        Returns:
            HTTP response.

        Raises:
            APIError: On HTTP status errors or network failures.
        """
        client = self._get_client()
        url = self._resolve_url(endpoint) if self._client else endpoint
        try:
            response = await client.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            logger.exception(
                "API HTTP error: %s - %s", exc.response.status_code, exc.response.text
            )
            raise APIError(
                f"HTTP error {exc.response.status_code} for {url}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            logger.exception("API request error: %s", exc)
            raise APIError(f"Request error for {url}: {exc}") from exc

    def validate_json_response(self, response: httpx.Response) -> dict[str, Any]:
        """Validate response is valid JSON.

        Args:
            response: HTTP response to validate.

        Returns:
            Parsed JSON as dictionary.

        Raises:
            APIError: If response body is not valid JSON.
        """
        try:
            return cast("dict[str, Any]", response.json())
        except json.JSONDecodeError as exc:
            logger.exception("Invalid JSON in response: %s", exc)
            raise APIError(f"Invalid JSON response: {exc}") from exc
