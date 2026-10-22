from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv

from models import MODEL_DEFAULT

load_dotenv()
client = Anthropic()


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(
    messages,
    model=MODEL_DEFAULT,
    max_tokens=1000,
    system=None,
    temperature=None,
    stop_sequences=None,
    tools=None,
    thinking=False,
    thinking_budget=1024,
    betas=None,
):
    params = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        params["system"] = system
    if temperature is not None:
        params["extra_body"] = {"temperature": temperature}
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    if tools:
        params["tools"] = tools
    if thinking:
        params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
    if betas:
        return client.beta.messages.create(**params, betas=betas)
    return client.messages.create(**params)


def chat_stream(
    messages,
    model=MODEL_DEFAULT,
    max_tokens=1000,
    system=None,
    temperature=None,
    stop_sequences=None,
    tools=None,
    tool_choice=None,
    betas=None,
):
    params = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        params["system"] = system
    if temperature is not None:
        params["extra_body"] = {"temperature": temperature}
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    if tools:
        params["tools"] = tools
    if tool_choice:
        params["tool_choice"] = tool_choice
    if betas:
        params["betas"] = betas
    return client.beta.messages.stream(**params)


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])
