# Module 5 - Simple Chatbot (`llm-chat`)

A small, multi-provider LLM client built **without frameworks** (no LangChain).
One entry point, `ask_llm()`, can call Gemini, OpenAI or Anthropic, either
through the official SDK or through raw HTTP, with input validation and a
retry policy that separates temporary failures from permanent ones.

> Status: **Topic 1 complete** (single LLM call).
> Next: **Topic 2** (conversation loop with memory).

## Why it is built this way

| Decision | Reason |
|---|---|
| `src/` layout | Code can only be imported once installed, so tests and CI use the same import path as real users. |
| One file per provider | Each provider has its own message format and exception types; the differences stay in one place. |
| Retry policy separate from provider code | One rule answers "is this failure temporary?" for every provider. |
| SDK retries switched off (`max_retries=0`) | `retry_call()` is the single retry owner; two retry systems never stack. |
| Only `cli.py` calls `input()` | Importing the package never prompts, so tests and a future Streamlit app can import it safely. |

## Layout

```
module-05-simple-chatbot/
├── pyproject.toml
├── .env.example            # names of the keys; real values go in .env (ignored)
├── src/llm_chat/
│   ├── errors.py           # custom exception family
│   ├── config.py           # provider settings, .env access
│   ├── validation.py       # prompt + output_type checks (no network)
│   ├── retry.py            # retry engine, backoff with full jitter
│   ├── providers/          # gemini / openai / anthropic (SDK + HTTP each)
│   ├── client.py           # ask_llm(): the single entry point
│   └── cli.py              # command-line runner
├── app/                    # Streamlit UI arrives in Topic 6
└── tests/                  # pytest, no network calls
```

## Setup

```powershell
uv sync
copy .env.example .env      # then add your key(s)
```

## Run

```powershell
uv run llm-chat             # or: uv run python -m llm_chat
```

## Test

```powershell
uv run pytest -q
```

## Known limitations (deliberate, fixed in later topics)

- `ask_llm()` returns a plain string for both replies and errors, so a caller
  cannot tell them apart by type. Topic 2 redesigns this contract.
- No conversation memory: every call is independent. Topic 2 adds it.
- A cut-off reply (`max_tokens`) is reported with a printed warning only.
