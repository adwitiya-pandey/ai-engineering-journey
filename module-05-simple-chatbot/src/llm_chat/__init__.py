"""llm_chat : a small multi-provider LLM client (Module 5)."""

from llm_chat.cli import main
from llm_chat.client import ask_llm

__all__ = ["ask_llm", "main"]
