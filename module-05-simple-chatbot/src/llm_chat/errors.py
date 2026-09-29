"""errors.py
============
The custom exceptions this project raises on purpose.

WHY ONE FILE FOR ERRORS: every other file (retry, providers, client)
needs to raise or catch these. Keeping them here means no file has to
import another just to share an error name.

WHY A FAMILY: all four inherit from LLMError, so a caller can catch
"any expected LLM problem" with one except clause, or catch a specific
one when it needs to react differently.
"""
from __future__ import annotations


class LLMError(RuntimeError):
    """Base class for every expected problem this project raises."""


class ConfigurationError(LLMError):
    """Something on YOUR machine is set up wrong, e.g. a missing API
    key or an unknown provider name. Retrying can never fix this."""


class InvalidInputError(LLMError):
    """What the CALLER passed in is unusable, e.g. a blank prompt or
    an unknown output_type. Detected BEFORE any network call."""


class ProviderRequestError(LLMError):
    """The provider rejected the request for a PERMANENT reason
    (bad request, invalid key, unknown model)."""


class RetryExhaustedError(LLMError):
    """A TEMPORARY failure kept happening through every retry."""
