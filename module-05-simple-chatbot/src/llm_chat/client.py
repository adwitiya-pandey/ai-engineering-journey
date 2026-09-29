"""client.py
===========
The single door into the project: ask_llm().

Everything else (validation, key lookup, provider choice, retries) is
wired together here ONCE, so every caller (the CLI today, Streamlit and
FastAPI later) gets the same safety checks without repeating them.

Topic 1 behaviour is preserved on purpose: ask_llm() returns a plain
string, and expected failures come back as "[...]" strings. Topic 2
(conversation memory) is where this contract gets redesigned.
"""
from __future__ import annotations

from llm_chat.config import (
    DEFAULT_METHOD,
    DEFAULT_PROVIDER,
    PROVIDER_CONFIG,
    VALID_METHODS,
    get_validated_api_key,
)
from llm_chat.errors import (
    ConfigurationError,
    ProviderRequestError,
    RetryExhaustedError,
)
from llm_chat.providers import (
    anthropic_provider,
    gemini_provider,
    openai_provider,
)
from llm_chat.validation import decide_max_tokens, validate_prompt

# provider name -> the module that knows how to talk to it.
# Keys must match PROVIDER_CONFIG in config.py.
_PROVIDER_MODULES = {
    "gemini": gemini_provider,
    "openai": openai_provider,
    "anthropic": anthropic_provider,
}


def _dispatch(
    provider: str,
    method: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> str:
    """Pick the right provider function and call it."""
    if method not in VALID_METHODS:
        valid = ", ".join(VALID_METHODS)
        raise ValueError(f"Unknown call method {method!r}. Valid choices: {valid}.")

    api_key = get_validated_api_key(provider)   # also checks the provider name
    module = _PROVIDER_MODULES[provider]
    call = module.call_sdk if method == "sdk" else module.call_http
    return call(
        api_key, PROVIDER_CONFIG[provider], system_prompt, user_prompt, max_tokens
    )


def ask_llm(
    system_prompt: str,
    user_prompt: str,
    output_type: str = "short_answer",
    provider: str = DEFAULT_PROVIDER,
    method: str = DEFAULT_METHOD,
) -> str:
    """Run one full LLM call.

    Returns the reply text on success, or a "[...]" message string for
    expected failures. Bad INPUT (blank prompt, unknown output_type)
    raises InvalidInputError before any network call is made.
    """
    max_tokens = decide_max_tokens(output_type)
    system_prompt = validate_prompt(system_prompt, "The System Prompt")
    user_prompt = validate_prompt(user_prompt, "The User Prompt")

    try:
        return _dispatch(provider, method, system_prompt, user_prompt, max_tokens)

    # ORDER MATTERS: most specific handler first, most general last.
    except ConfigurationError as e:
        return f"[Configuration error: {e}]"
    except ProviderRequestError as e:
        # e.__cause__ holds the original SDK/HTTP error with the detail.
        return f"[Request rejected: {e} Cause: {e.__cause__}]"
    except RetryExhaustedError as e:
        return f"[Provider unavailable after retries: {e}]"
    except ValueError as e:
        return f"[Setup error: {e}]"
