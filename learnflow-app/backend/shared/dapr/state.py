"""
Dapr State Store Utilities

Helpers for get, set, and delete operations on Dapr state store.
"""

import logging
from typing import Any, Optional, TypeVar

import httpx
from pydantic import BaseModel

from ..config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


async def get_state(
    key: str,
    store_name: Optional[str] = None,
    model_class: Optional[type[T]] = None,
) -> Optional[T | dict[str, Any]]:
    """
    Get state from Dapr state store.

    Args:
        key: The state key to retrieve
        store_name: The state store component name
        model_class: Optional Pydantic model to parse the result

    Returns:
        The state value (as dict or Pydantic model), or None if not found
    """
    store = store_name or settings.dapr_statestore_name
    url = f"http://localhost:{settings.dapr_http_port}/v1.0/state/{store}/{key}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)

            if response.status_code == 204:
                return None

            response.raise_for_status()
            data = response.json()

            if model_class:
                return model_class.model_validate(data)
            return data

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        logger.error(f"Failed to get state for key {key}: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to get state for key {key}: {e}")
        raise


async def save_state(
    key: str,
    value: BaseModel | dict[str, Any],
    store_name: Optional[str] = None,
    etag: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> bool:
    """
    Save state to Dapr state store.

    Args:
        key: The state key
        value: The value to store (Pydantic model or dict)
        store_name: The state store component name
        etag: Optional ETag for optimistic concurrency
        metadata: Optional metadata

    Returns:
        True if saved successfully, False otherwise
    """
    store = store_name or settings.dapr_statestore_name
    url = f"http://localhost:{settings.dapr_http_port}/v1.0/state/{store}"

    # Convert Pydantic model to dict
    if isinstance(value, BaseModel):
        data = value.model_dump(mode="json")
    else:
        data = value

    state_item = {
        "key": key,
        "value": data,
    }

    if etag:
        state_item["etag"] = etag

    if metadata:
        state_item["metadata"] = metadata

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=[state_item],
                timeout=10.0,
            )
            response.raise_for_status()
            logger.debug(f"Saved state for key {key}")
            return True
    except Exception as e:
        logger.error(f"Failed to save state for key {key}: {e}")
        return False


async def delete_state(
    key: str,
    store_name: Optional[str] = None,
    etag: Optional[str] = None,
) -> bool:
    """
    Delete state from Dapr state store.

    Args:
        key: The state key to delete
        store_name: The state store component name
        etag: Optional ETag for optimistic concurrency

    Returns:
        True if deleted successfully, False otherwise
    """
    store = store_name or settings.dapr_statestore_name
    url = f"http://localhost:{settings.dapr_http_port}/v1.0/state/{store}/{key}"

    headers = {}
    if etag:
        headers["If-Match"] = etag

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            logger.debug(f"Deleted state for key {key}")
            return True
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return True  # Already deleted
        logger.error(f"Failed to delete state for key {key}: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to delete state for key {key}: {e}")
        return False


async def bulk_get_state(
    keys: list[str],
    store_name: Optional[str] = None,
) -> dict[str, Any]:
    """
    Get multiple state values in a single request.

    Args:
        keys: List of state keys to retrieve
        store_name: The state store component name

    Returns:
        Dictionary mapping keys to their values
    """
    store = store_name or settings.dapr_statestore_name
    url = f"http://localhost:{settings.dapr_http_port}/v1.0/state/{store}/bulk"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={"keys": keys},
                timeout=10.0,
            )
            response.raise_for_status()
            items = response.json()
            return {item["key"]: item.get("data") for item in items}
    except Exception as e:
        logger.error(f"Failed to bulk get state: {e}")
        raise
