"""Mock-test the `chat_tools.chat` wrapper and the `text_from_message` helper.

Replaces the module-level Anthropic client with a `MagicMock`, calls the wrapper, and asserts
on the params it would have sent and which client method it used. No API call is made.
"""

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

import chat_tools


@pytest.fixture
def mock_client() -> Iterator[MagicMock]:
    with patch.object(chat_tools, "client") as client:
        yield client


def test_chat_uses_messages_create_when_no_betas(mock_client: MagicMock) -> None:
    chat_tools.chat([{"role": "user", "content": "hi"}])
    mock_client.messages.create.assert_called_once()
    mock_client.beta.messages.create.assert_not_called()


def test_chat_uses_beta_messages_create_when_betas_set(mock_client: MagicMock) -> None:
    chat_tools.chat(
        [{"role": "user", "content": "hi"}],
        betas=["prompt-caching-2024-07-31"],
    )
    mock_client.beta.messages.create.assert_called_once()
    mock_client.messages.create.assert_not_called()
    kwargs = mock_client.beta.messages.create.call_args.kwargs
    assert kwargs["betas"] == ["prompt-caching-2024-07-31"]


def test_chat_adds_thinking_block_with_default_budget(mock_client: MagicMock) -> None:
    chat_tools.chat([{"role": "user", "content": "hi"}], thinking=True)
    kwargs = mock_client.messages.create.call_args.kwargs
    assert kwargs["thinking"] == {"type": "enabled", "budget_tokens": 1024}


def test_chat_adds_thinking_block_with_custom_budget(mock_client: MagicMock) -> None:
    chat_tools.chat(
        [{"role": "user", "content": "hi"}],
        thinking=True,
        thinking_budget=5000,
    )
    kwargs = mock_client.messages.create.call_args.kwargs
    assert kwargs["thinking"]["budget_tokens"] == 5000


def test_chat_passes_tools_when_set(mock_client: MagicMock) -> None:
    tools = [{"name": "get_weather", "description": "...", "input_schema": {}}]
    chat_tools.chat([{"role": "user", "content": "hi"}], tools=tools)
    kwargs = mock_client.messages.create.call_args.kwargs
    assert kwargs["tools"] == tools


def test_chat_omits_optional_params_when_not_set(mock_client: MagicMock) -> None:
    chat_tools.chat([{"role": "user", "content": "hi"}])
    kwargs = mock_client.messages.create.call_args.kwargs
    for name in ("extra_body", "stop_sequences", "system", "thinking", "tools"):
        assert name not in kwargs


def test_text_from_message_joins_text_blocks_only() -> None:
    message = MagicMock()
    text_a = MagicMock(type="text")
    text_a.text = "hello"
    tool = MagicMock(type="tool_use")
    text_b = MagicMock(type="text")
    text_b.text = "world"
    message.content = [text_a, tool, text_b]

    assert chat_tools.text_from_message(message) == "hello\nworld"
