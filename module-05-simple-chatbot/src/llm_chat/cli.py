"""cli.py
========
The command-line runner. This is the ONLY file allowed to ask the user
questions with input(). Run it with either:

    uv run llm-chat
    uv run python -m llm_chat
"""

from __future__ import annotations

import logging

from llm_chat.client import ask_llm
from llm_chat.errors import InvalidInputError


def main() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    provider = (
        input("Which llm provider do you want to use [gemini, openai, anthropic]? ")
        .strip()
        .lower()
    )
    method = input("How do you want to call the llm [sdk, http]? ").strip().lower()
    system_prompt = input("Who do you want the llm to act like? ")
    user_prompt = input("What is your question? ")
    output_type = input(
        "How detailed do you want the output [short_answer, summary, code, long_form]? "
    )

    try:
        reply = ask_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_type=output_type,
            provider=provider,
            method=method,
        )
    except InvalidInputError as e:
        print(f"[Input error: {e}]")
        return

    print(reply)


if __name__ == "__main__":
    main()
