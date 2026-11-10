"""Mock-test the `chat.chat` wrapper.

Replaces the module-level Anthropic client with a `MagicMock`, calls the wrapper, and asserts on
the params it would have sent and the value it returns. No API call is made.
"""

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

import chat


def _mock_response(text: str) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock(text=text)]
    return response


@pytest.fixture
def mock_client() -> Iterator[MagicMock]:
    with patch.object(chat, "client") as client:
        yield client


def test_strips_surrounding_whitespace_from_response(mock_client: MagicMock) -> None:
    mock_client.messages.create.return_value = _mock_response("  hello  ")
    result = chat.chat([{"role": "user", "content": "hi"}])
    assert result == "hello"


def test_passes_required_params(mock_client: MagicMock) -> None:
    mock_client.messages.create.return_value = _mock_response("")
    messages = [{"role": "user", "content": "hi"}]
    chat.chat(messages, model="claude-haiku-4-5", max_tokens=42)
    kwargs = mock_client.messages.create.call_args.kwargs
    assert kwargs["model"] == "claude-haiku-4-5"
    assert kwargs["max_tokens"] == 42
    assert kwargs["messages"] == messages


def test_routes_temperature_through_extra_body(mock_client: MagicMock) -> None:
    mock_client.messages.create.return_value = _mock_response("")
    chat.chat([{"role": "user", "content": "hi"}], temperature=0.7)
    kwargs = mock_client.messages.create.call_args.kwargs
    assert kwargs["extra_body"] == {"temperature": 0.7}
    assert "temperature" not in kwargs


def test_omits_optional_params_when_not_set(mock_client: MagicMock) -> None:
    mock_client.messages.create.return_value = _mock_response("")
    chat.chat([{"role": "user", "content": "hi"}])
    kwargs = mock_client.messages.create.call_args.kwargs
    for name in ("extra_body", "stop_sequences", "system"):
        assert name not in kwargs


def test_passes_system_and_stop_sequences(mock_client: MagicMock) -> None:
    mock_client.messages.create.return_value = _mock_response("")
    chat.chat(
        [{"role": "user", "content": "hi"}],
        system="You are helpful.",
        stop_sequences=["</end>"],
    )
    kwargs = mock_client.messages.create.call_args.kwargs
    assert kwargs["system"] == "You are helpful."
    assert kwargs["stop_sequences"] == ["</end>"]
