"""retry.py
==========
Retry policy only: WHEN to retry, HOW LONG to wait, and which failures
are worth retrying at all. Nothing here knows about prompts or what a
"reply" looks like.

The core question answered before every retry: "Is this failure
temporary?"
    429 rate limited, 5xx server trouble, timeouts -> yes, retry
    401 invalid key, 400 malformed request          -> NO, fail fast

Provider-specific classifiers (which SDK exception means what) live
next to each provider in providers/. Only the generic pieces are here.
"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

from llm_chat.errors import ProviderRequestError, RetryExhaustedError

LOGGER = logging.getLogger(__name__)

# 408 timeout, 409 conflict, 429 rate limited (5xx handled separately).
RETRYABLE_HTTP_STATUS_CODES = frozenset({408, 409, 429})


@dataclass(frozen=True)
class RetryConfig:
    """A labelled bundle of retry settings.

    max_attempts includes the FIRST try: 5 means one try + up to 4 retries.
    """

    max_attempts: int = 5
    base_delay: float = 1.0  # first retry waits around this long
    max_delay: float = 20.0  # no wait ever exceeds this

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.base_delay <= 0:
            raise ValueError("base_delay must be > 0")
        if self.max_delay < self.base_delay:
            raise ValueError("max_delay must be >= base_delay")


DEFAULT_RETRY_CONFIG = RetryConfig()

T = TypeVar("T")


def retry_call(
    operation: Callable[[], T],
    *,
    provider: str,
    is_retryable: Callable[[BaseException], bool],
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
) -> T:
    """Run operation(); retry temporary failures with jittered backoff.

    Raises:
        ProviderRequestError: the failure was permanent, not retried.
        RetryExhaustedError:  temporary failure persisted through
                              every allowed attempt.
    """
    for attempt in range(1, config.max_attempts + 1):
        try:
            return operation()
        except Exception as exc:
            if not is_retryable(exc):
                raise ProviderRequestError(
                    f"{provider} request failed: {type(exc).__name__}."
                ) from exc

            if attempt == config.max_attempts:
                raise RetryExhaustedError(
                    f"{provider} request failed after {config.max_attempts} attempts."
                ) from exc

            delay = _retry_delay(attempt, exc, config)
            LOGGER.warning(
                "%s request failed with %s (attempt %d/%d); retrying in %.1fs.",
                provider,
                type(exc).__name__,
                attempt,
                config.max_attempts,
                delay,
            )
            time.sleep(delay)

    # Structurally unreachable; keeps linters and future readers calm.
    raise AssertionError("Retry loop terminated unexpectedly.")


def _retry_delay(attempt: int, exc: BaseException, config: RetryConfig) -> float:
    """How long to wait before the NEXT attempt."""
    retry_after = _retry_after_seconds(exc, config.max_delay)
    if retry_after is not None:
        return retry_after

    exponential_ceiling = min(
        config.max_delay,
        config.base_delay * (2 ** (attempt - 1)),
    )
    # FULL JITTER: a random wait anywhere in [0, ceiling]. It spreads
    # out many clients that failed at the same moment ("thundering
    # herd"). Trade-off: a retry can occasionally fire almost at once.
    return random.uniform(0, exponential_ceiling)


def _retry_after_seconds(exc: BaseException, max_delay: float) -> float | None:
    """Honour a numeric 'Retry-After' header when the provider sends one."""
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)
    if not headers:
        return None

    value = headers.get("retry-after")
    if value is None:
        return None
    try:
        delay = float(value)
    except (TypeError, ValueError):
        return None

    if 0 < delay <= max_delay:
        return delay
    return None


# ---------------------------------------------------------------------
# SHARED CLASSIFIERS (used by more than one provider)
# ---------------------------------------------------------------------


def is_retryable_http_status(status: object) -> bool:
    """True for 408, 409, 429 or any 5xx status code."""
    return isinstance(status, int) and (
        status in RETRYABLE_HTTP_STATUS_CODES or status >= 500
    )


def is_retryable_transport_error(exc: BaseException) -> bool:
    """True for low-level network failures (timeout, dropped connection)."""
    try:
        import httpx
    except ImportError:
        httpx = None

    if httpx is not None and isinstance(
        exc, (httpx.TimeoutException, httpx.NetworkError)
    ):
        return True
    return isinstance(exc, (TimeoutError, ConnectionError))


def is_http_retryable(exc: BaseException) -> bool:
    """Classifier for the raw-HTTP path (the `requests` library), which
    fails the same way for all three providers."""
    import requests

    if isinstance(exc, requests.HTTPError):
        status_code = exc.response.status_code if exc.response is not None else None
        return is_retryable_http_status(status_code)

    if isinstance(exc, (requests.ConnectionError, requests.Timeout)):
        return True
    return False
