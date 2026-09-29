"""anthropic_provider.py : Anthropic, via SDK and via raw HTTP."""
from __future__ import annotations

import requests

from llm_chat.providers._shared import HTTP_TIMEOUT_SECONDS, warn_truncated
from llm_chat.retry import (
    DEFAULT_RETRY_CONFIG,
    is_http_retryable,
    is_retryable_http_status,
    retry_call,
)

ANTHROPIC_API_VERSION = "2023-06-01"


def is_anthropic_retryable(exc: BaseException) -> bool:
    """True for Anthropic failures worth retrying."""
    try:
        import anthropic
    except ImportError:
        return False

    if isinstance(
        exc,
        (
            anthropic.APIConnectionError,
            anthropic.APITimeoutError,
            anthropic.RateLimitError,
            anthropic.InternalServerError,
        ),
    ):
        return True
    if isinstance(exc, anthropic.APIStatusError):
        return is_retryable_http_status(getattr(exc, "status_code", None))
    return False


def call_sdk(
    api_key: str,
    settings: dict[str, str],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> str:
    import anthropic

    # max_retries=0: retry_call() stays the single retry owner.
    client = anthropic.Anthropic(api_key=api_key, max_retries=0)

    def do_call() -> str:
        response = client.messages.create(
            model=settings["model"],
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        if response.stop_reason == "max_tokens":
            warn_truncated()
        return response.content[0].text

    return retry_call(
        do_call,
        provider="Anthropic",
        is_retryable=is_anthropic_retryable,
        config=DEFAULT_RETRY_CONFIG,
    )


def call_http(
    api_key: str,
    settings: dict[str, str],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> str:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_API_VERSION,
        "content-type": "application/json",
    }
    body = {
        "model": settings["model"],
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    def do_call() -> str:
        resp = requests.post(
            settings["http_url"],
            headers=headers,
            json=body,
            timeout=HTTP_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("stop_reason") == "max_tokens":
            warn_truncated()
        return data["content"][0]["text"]

    return retry_call(
        do_call,
        provider="Anthropic (HTTP)",
        is_retryable=is_http_retryable,
        config=DEFAULT_RETRY_CONFIG,
    )
