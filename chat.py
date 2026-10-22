from anthropic import Anthropic
from dotenv import find_dotenv, load_dotenv

from models import MODEL_DEFAULT

load_dotenv(find_dotenv())
client = Anthropic()


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(messages, model=MODEL_DEFAULT, max_tokens=1000, system=None, temperature=None, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system:
        params["system"] = system
    if temperature is not None:
        params["extra_body"] = {"temperature": temperature}
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    response = client.messages.create(**params)
    return response.content[0].text.strip()
