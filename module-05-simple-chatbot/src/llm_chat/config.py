"""config.py
===========
Settings and environment access. No network calls and no prompts to
the user happen here, so importing this file is always safe.

Compared with the single-file version, two things changed:
  * PROVIDER and CALL_METHOD are no longer read with input() at import
    time. Only cli.py is allowed to ask the user questions. A file that
    prompts on import cannot be used by tests or by Streamlit (Topic 6).
  * load_dotenv() runs when a key is requested, not at import.
"""

from __future__ import annotations

import os

from dotenv import find_dotenv, load_dotenv

from llm_chat.errors import ConfigurationError

DEFAULT_PROVIDER = "gemini"
DEFAULT_METHOD = "sdk"
VALID_METHODS = ("sdk", "http")

# One entry per provider. Adding a provider = adding an entry here
# plus one file in providers/.
PROVIDER_CONFIG: dict[str, dict[str, str]] = {
    "gemini": {
        "env_key_name": "GOOGLE_API_KEY",
        "model": "gemini-3.8-flash",
        "http_url": (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-3.8-flash:generateContent"
        ),
    },
    "openai": {
        "env_key_name": "OPENAI_API_KEY",
        "model": "gpt-4o",
        "http_url": "https://api.openai.com/v1/chat/completions",
    },
    "anthropic": {
        "env_key_name": "ANTHROPIC_API_KEY",
        "model": "claude-sonnet-4-20250514",
        "http_url": "https://api.anthropic.com/v1/messages",
    },
}


def get_required_env(name: str) -> str:
    """Read one environment variable; fail loudly if missing/blank."""
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigurationError(
            f"Required environment variable {name!r} is not set. Check your .env file."
        )
    return value


def get_validated_api_key(provider: str) -> str:
    """Validate the provider name, load .env, return that provider's key."""
    if provider not in PROVIDER_CONFIG:
        valid = ", ".join(PROVIDER_CONFIG)
        raise ConfigurationError(
            f"Unknown provider {provider!r}. Valid choices: {valid}."
        )
    # usecwd=True searches for .env starting from the folder you run
    # the command in. Existing environment variables are NOT overridden.
    load_dotenv(find_dotenv(usecwd=True))
    return get_required_env(PROVIDER_CONFIG[provider]["env_key_name"])
