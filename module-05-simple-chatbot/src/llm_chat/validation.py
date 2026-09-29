"""validation.py
===============
Input checks that run BEFORE any network call, so a mistake costs zero
time and zero money.
"""
from __future__ import annotations

from llm_chat.errors import InvalidInputError

# How many tokens of reply to allow for each kind of task.
OUTPUT_BUDGETS: dict[str, int] = {
    "short_answer": 100,   # a sentence or two
    "summary": 400,        # a paragraph
    "code": 1500,          # a snippet or short script
    "long_form": 2000,     # essays, detailed explanations
}


def decide_max_tokens(expected_output_type: str) -> int:
    """Strict lookup: an unknown output type is an error, never a guess."""
    cleaned = (
        expected_output_type.strip()
        if isinstance(expected_output_type, str)
        else ""
    )
    if cleaned not in OUTPUT_BUDGETS:
        valid = ", ".join(OUTPUT_BUDGETS)
        raise InvalidInputError(
            f"Unknown output_type {expected_output_type!r}. "
            f"Valid choices: {valid}."
        )
    return OUTPUT_BUDGETS[cleaned]


def validate_prompt(value: object, field_name: str) -> str:
    """Return the prompt stripped of surrounding whitespace, or raise
    InvalidInputError if it is not text or is blank."""
    if not isinstance(value, str):
        raise InvalidInputError(
            f"{field_name} must be text, got {type(value).__name__}."
        )
    cleaned = value.strip()
    if not cleaned:
        raise InvalidInputError(
            f"{field_name} is empty or only whitespace. "
            f"Nothing was sent to the provider."
        )
    return cleaned
