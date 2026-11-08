"""Thin wrapper around the Anthropic SDK.

The `Claude` class holds the SDK client and exposes `chat` (non-streaming in this demo).
Module-level helpers (`add_user_message`, `add_assistant_message`, `text_from_message`)
manipulate the messages list without needing a `Claude` instance.
"""

from anthropic import Anthropic
from anthropic.types import Message


def add_user_message(messages: list, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages: list, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def text_from_message(message: Message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


class Claude:
    def __init__(self, model: str):
        self.client = Anthropic()
        self.model = model

    def chat(
        self,
        messages,
        system=None,
        temperature=None,
        stop_sequences=None,
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
        }

        if temperature is not None:
            params["extra_body"] = {"temperature": temperature}

        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message = self.client.messages.create(**params)
        return message
