"""Small helpers shared by every provider module."""

from __future__ import annotations

HTTP_TIMEOUT_SECONDS = 30


def warn_truncated() -> None:
    """Tell the user a reply stopped because it hit max_tokens."""
    print(
        "  Warning: reply was cut off - it hit max_tokens. "
        "Consider raising max_tokens for this task type."
    )
