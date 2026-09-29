import pytest
import requests

from llm_chat import retry
from llm_chat.errors import ProviderRequestError, RetryExhaustedError
from llm_chat.retry import (
    RetryConfig,
    is_http_retryable,
    is_retryable_http_status,
    retry_call,
)


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    """Never really wait during tests; record the requested delays."""
    delays = []
    monkeypatch.setattr(retry.time, "sleep", delays.append)
    return delays


def test_success_on_first_try(no_sleep):
    result = retry_call(lambda: "ok", provider="T", is_retryable=lambda e: True)
    assert result == "ok"
    assert no_sleep == []


def test_temporary_failure_then_success(no_sleep):
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TimeoutError("blip")
        return "recovered"

    result = retry_call(flaky, provider="T", is_retryable=lambda e: True)
    assert result == "recovered"
    assert calls["n"] == 3
    assert len(no_sleep) == 2


def test_permanent_error_fails_fast_without_sleeping(no_sleep):
    def bad_key():
        raise PermissionError("invalid key")

    with pytest.raises(ProviderRequestError) as info:
        retry_call(bad_key, provider="T", is_retryable=lambda e: False)
    assert isinstance(info.value.__cause__, PermissionError)
    assert no_sleep == []


def test_exhausted_after_max_attempts(no_sleep):
    cfg = RetryConfig(max_attempts=3)

    def always_fails():
        raise TimeoutError("down")

    with pytest.raises(RetryExhaustedError):
        retry_call(always_fails, provider="T", is_retryable=lambda e: True, config=cfg)
    assert len(no_sleep) == 2   # sleeps between attempts, not after the last


def test_retry_after_header_is_honoured(no_sleep):
    class Resp:
        headers = {"retry-after": "3"}

    class Err(Exception):
        response = Resp()

    calls = {"n": 0}

    def once_then_ok():
        calls["n"] += 1
        if calls["n"] == 1:
            raise Err()
        return "ok"

    retry_call(once_then_ok, provider="T", is_retryable=lambda e: True)
    assert no_sleep == [3.0]


@pytest.mark.parametrize(
    "kwargs",
    [{"max_attempts": 0}, {"base_delay": 0}, {"base_delay": 5, "max_delay": 1}],
)
def test_retry_config_rejects_bad_numbers(kwargs):
    with pytest.raises(ValueError):
        RetryConfig(**kwargs)


@pytest.mark.parametrize(
    "status, expected",
    [(408, True), (429, True), (500, True), (503, True), (400, False), (401, False), (None, False)],
)
def test_http_status_classification(status, expected):
    assert is_retryable_http_status(status) is expected


def _http_error(status):
    resp = requests.Response()
    resp.status_code = status
    return requests.HTTPError(response=resp)


def test_http_retryable_for_429_but_not_401():
    assert is_http_retryable(_http_error(429)) is True
    assert is_http_retryable(_http_error(401)) is False
    assert is_http_retryable(requests.ConnectionError()) is True
    assert is_http_retryable(ValueError("x")) is False
