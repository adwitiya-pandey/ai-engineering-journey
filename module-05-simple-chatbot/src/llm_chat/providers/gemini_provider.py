"""gemini_provider.py : Google Gemini, via SDK and via raw HTTP."""

from __future__ import annotations

import requests

from llm_chat.providers._shared import HTTP_TIMEOUT_SECONDS, warn_truncated
from llm_chat.retry import (
    DEFAULT_RETRY_CONFIG,
    is_http_retryable,
    is_retryable_http_status,
    is_retryable_transport_error,
    retry_call,
)

BLOCKED_MESSAGE = "[Response blocked by Gemini's safety filter]"


def is_gemini_retryable(exc: BaseException) -> bool:
    """True for Gemini failures worth retrying (server errors, rate
    limits, network blips). False for e.g. invalid key or bad request."""
    try:
        from google.genai.errors import ClientError, ServerError
    except ImportError:
        return False

    if isinstance(exc, ServerError):
        return True
    if isinstance(exc, ClientError):
        return is_retryable_http_status(getattr(exc, "code", None))
    return is_retryable_transport_error(exc)


def call_sdk(
    api_key: str,
    settings: dict[str, str],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    def do_call() -> str:
        response = client.models.generate_content(
            model=settings["model"],
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=max_tokens,
            ),
        )
        # Check finish_reason BEFORE response.text: a safety block makes
        # response.text raise instead of returning text.
        finish_reason = response.candidates[0].finish_reason.name
        if finish_reason == "SAFETY":
            return BLOCKED_MESSAGE
        if finish_reason == "MAX_TOKENS":
            warn_truncated()
        return response.text

    return retry_call(
        do_call,
        provider="Gemini",
        is_retryable=is_gemini_retryable,
        config=DEFAULT_RETRY_CONFIG,
    )


def call_http(
    api_key: str,
    settings: dict[str, str],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> str:
    url = f"{settings['http_url']}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    body = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }

    def do_call() -> str:
        resp = requests.post(
            url, headers=headers, json=body, timeout=HTTP_TIMEOUT_SECONDS
        )
        resp.raise_for_status()
        candidate = resp.json()["candidates"][0]
        finish_reason = candidate.get("finishReason", "")

        if finish_reason == "SAFETY":
            return BLOCKED_MESSAGE
        if finish_reason == "MAX_TOKENS":
            warn_truncated()
        return candidate["content"]["parts"][0]["text"]

    return retry_call(
        do_call,
        provider="Gemini (HTTP)",
        is_retryable=is_http_retryable,
        config=DEFAULT_RETRY_CONFIG,
    )
