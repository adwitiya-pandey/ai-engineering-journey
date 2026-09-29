import pytest

from llm_chat.errors import InvalidInputError
from llm_chat.validation import decide_max_tokens, validate_prompt


@pytest.mark.parametrize(
    "output_type, expected",
    [("short_answer", 100), ("summary", 400), ("code", 1500), ("long_form", 2000)],
)
def test_decide_max_tokens_known_types(output_type, expected):
    assert decide_max_tokens(output_type) == expected


def test_decide_max_tokens_strips_whitespace():
    assert decide_max_tokens("  summary  ") == 400


@pytest.mark.parametrize("bad", ["sumary", "", None, 42])
def test_decide_max_tokens_rejects_unknown(bad):
    with pytest.raises(InvalidInputError):
        decide_max_tokens(bad)


def test_validate_prompt_strips():
    assert validate_prompt("  hello  ", "Prompt") == "hello"


@pytest.mark.parametrize("bad", ["", "   ", "\n\t", None, 7])
def test_validate_prompt_rejects_blank_or_non_text(bad):
    with pytest.raises(InvalidInputError):
        validate_prompt(bad, "Prompt")
