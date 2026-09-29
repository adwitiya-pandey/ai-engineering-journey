"""openai_provider.py : OpenAI, via SDK and via raw HTTP."""
from __future__ import annotations

import requests

from llm_chat.providers._shared import HTTP_TIMEOUT_SECONDS, warn_truncated
from llm_chat.retry import (
    DEFAULT_RETRY_CONFIG,
    is_http_retryable,
    is_retryable_http_status,
    retry_call,
)


def is_openai_retryable(exc: BaseException) -> bool:
    """True for OpenAI failures worth retrying."""
    try:
        import openai
    except ImportError:
        return False

    if isinstance(
        exc,
        (
            openai.APIConnectionError,
            openai.APITimeoutError,
            openai.RateLimitError,
            openai.InternalServerError,
        ),
    ):
        return True
    if isinstance(exc, openai.APIStatusError):
        return is_retryable_http_status(getattr(exc, "status_code", None))
    # AuthenticationError, BadRequestError, etc. are PERMANENT.
    return False


def call_sdk(
    api_key: str,
    settings: dict[str, str],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> str:
    from openai import OpenAI

    # max_retries=0 switches OFF the SDK's own retries so retry_call()
    # is the single retry owner (no two retry systems stacking up).
    client = OpenAI(api_key=api_key, max_retries=0)

    def do_call() -> str:
        response = client.chat.completions.create(
            model=settings["model"],
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        choice = response.choices[0]
        if choice.finish_reason == "length":
            warn_truncated()
        return choice.message.content

    return retry_call(
        do_call,
        provider="OpenAI",
        is_retryable=is_openai_retryable,
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
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings["model"],
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    def do_call() -> str:
        resp = requests.post(
            settings["http_url"],
            headers=headers,
            json=body,
            timeout=HTTP_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        choice = resp.json()["choices"][0]
        if choice.get("finish_reason") == "length":
            warn_truncated()
        return choice["message"]["content"]

    return retry_call(
        do_call,
        provider="OpenAI (HTTP)",
        is_retryable=is_http_retryable,
        config=DEFAULT_RETRY_CONFIG,
    )
