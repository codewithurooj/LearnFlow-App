"""
Dapr Pub/Sub Utilities

Helpers for publishing events and subscribing to topics via Dapr.
"""

import logging
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

import httpx
from pydantic import BaseModel

from ..config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


async def publish_event(
    topic: str,
    data: BaseModel | dict[str, Any],
    pubsub_name: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> bool:
    """
    Publish an event to a Dapr pub/sub topic.

    Args:
        topic: The topic name to publish to
        data: The event data (Pydantic model or dict)
        pubsub_name: The pub/sub component name (defaults to config)
        metadata: Optional metadata for the event

    Returns:
        True if published successfully, False otherwise
    """
    pubsub = pubsub_name or settings.dapr_pubsub_name
    url = f"http://localhost:{settings.dapr_http_port}/v1.0/publish/{pubsub}/{topic}"

    # Convert Pydantic model to dict
    if isinstance(data, BaseModel):
        payload = data.model_dump(mode="json")
    else:
        payload = data

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"Published event to {topic}: {payload.get('event_id', 'unknown')}")
            return True
    except Exception as e:
        logger.error(f"Failed to publish event to {topic}: {e}")
        return False


def subscribe_handler(
    topic: str,
    pubsub_name: Optional[str] = None,
    route: Optional[str] = None,
) -> Callable:
    """
    Decorator to mark a function as a Dapr subscription handler.

    This decorator adds metadata that can be used to register
    subscriptions with Dapr. The actual subscription registration
    happens in the FastAPI app setup.

    Args:
        topic: The topic name to subscribe to
        pubsub_name: The pub/sub component name
        route: The HTTP route for the handler

    Returns:
        Decorated function with subscription metadata
    """
    pubsub = pubsub_name or settings.dapr_pubsub_name

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await func(*args, **kwargs)

        # Attach subscription metadata
        wrapper._dapr_subscription = {
            "pubsubname": pubsub,
            "topic": topic,
            "route": route or f"/events/{topic.replace('.', '-')}",
        }
        return wrapper

    return decorator


def get_subscriptions(handlers: list[Callable]) -> list[dict[str, str]]:
    """
    Extract subscription declarations from handler functions.

    This is used to build the response for /dapr/subscribe endpoint.

    Args:
        handlers: List of handler functions decorated with @subscribe_handler

    Returns:
        List of subscription declarations for Dapr
    """
    subscriptions = []
    for handler in handlers:
        if hasattr(handler, "_dapr_subscription"):
            subscriptions.append(handler._dapr_subscription)
    return subscriptions


class CloudEvent(BaseModel):
    """CloudEvents envelope for Dapr pub/sub messages."""

    id: str
    source: str
    type: str
    specversion: str = "1.0"
    datacontenttype: str = "application/json"
    data: dict[str, Any]

    @classmethod
    def parse_event(cls, raw: dict[str, Any], model_class: type[T]) -> T:
        """Parse a CloudEvent and extract the typed data."""
        event = cls.model_validate(raw)
        return model_class.model_validate(event.data)
