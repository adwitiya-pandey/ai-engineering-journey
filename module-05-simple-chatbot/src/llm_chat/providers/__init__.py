"""providers/ : one file per LLM company.

Every provider module exposes the same two functions:
    call_sdk(api_key, settings, system_prompt, user_prompt, max_tokens) -> str
    call_http(api_key, settings, system_prompt, user_prompt, max_tokens) -> str
so client.py can treat them interchangeably.
"""
