"""Characterisation tests: they pin down what ask_llm() does TODAY
(Topic 1 behaviour) so Topic 2 changes cannot break it silently.
No network calls; providers are replaced with fakes."""
import pytest

from llm_chat import client, config
from llm_chat.errors import (
    InvalidInputError,
    ProviderRequestError,
    RetryExhaustedError,
)


@pytest.fixture(autouse=True)
def fake_key(monkeypatch):
    """Pretend .env has every key, and never read a real .env file."""
    monkeypatch.setattr(config, "load_dotenv", lambda *a, **k: False)
    for name in ("GOOGLE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.setenv(name, "test-key")


def _patch_call(monkeypatch, provider, which, fn):
    monkeypatch.setattr(client._PROVIDER_MODULES[provider], which, fn)


def test_returns_reply_text_on_success(monkeypatch):
    seen = {}

    def fake_sdk(api_key, settings, system_prompt, user_prompt, max_tokens):
        seen.update(key=api_key, system=system_prompt, user=user_prompt, tokens=max_tokens)
        return "Hello Priya!"

    _patch_call(monkeypatch, "gemini", "call_sdk", fake_sdk)
    reply = client.ask_llm("  Be kind  ", "  Hi  ", output_type="summary")

    assert reply == "Hello Priya!"
    assert seen == {"key": "test-key", "system": "Be kind", "user": "Hi", "tokens": 400}


def test_http_method_uses_call_http(monkeypatch):
    _patch_call(monkeypatch, "openai", "call_http", lambda *a: "via http")
    assert client.ask_llm("s", "u", provider="openai", method="http") == "via http"


def test_unknown_method_returns_setup_error():
    reply = client.ask_llm("s", "u", method="carrier-pigeon")
    assert reply.startswith("[Setup error:")


def test_unknown_provider_returns_configuration_error():
    reply = client.ask_llm("s", "u", provider="gemni")
    assert reply.startswith("[Configuration error:")
    assert "gemni" in reply


def test_missing_key_returns_configuration_error(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY")
    reply = client.ask_llm("s", "u")
    assert reply.startswith("[Configuration error:")


def test_permanent_provider_error_message_includes_cause(monkeypatch):
    def rejects(*args):
        raise ProviderRequestError("Gemini request failed: ClientError.") from ValueError("401 bad key")

    _patch_call(monkeypatch, "gemini", "call_sdk", rejects)
    reply = client.ask_llm("s", "u")
    assert reply.startswith("[Request rejected:")
    assert "401 bad key" in reply


def test_exhausted_retries_message(monkeypatch):
    def exhausted(*args):
        raise RetryExhaustedError("Gemini request failed after 5 attempts.")

    _patch_call(monkeypatch, "gemini", "call_sdk", exhausted)
    assert client.ask_llm("s", "u").startswith("[Provider unavailable after retries:")


def test_blank_prompt_raises_before_any_call(monkeypatch):
    def must_not_run(*args):
        raise AssertionError("provider was called for a blank prompt")

    _patch_call(monkeypatch, "gemini", "call_sdk", must_not_run)
    with pytest.raises(InvalidInputError):
        client.ask_llm("s", "   ")


def test_unknown_output_type_raises():
    with pytest.raises(InvalidInputError):
        client.ask_llm("s", "u", output_type="essay")


def test_current_limitation_error_and_reply_are_both_plain_strings(monkeypatch):
    """DOCUMENTS the Topic 1 weakness that Topic 2 must fix: a caller
    cannot tell a real reply from an error message by type alone."""
    _patch_call(monkeypatch, "gemini", "call_sdk", lambda *a: "real reply")
    ok = client.ask_llm("s", "u")
    err = client.ask_llm("s", "u", method="nope")
    assert type(ok) is type(err) is str
