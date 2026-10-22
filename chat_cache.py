"""Chat wrapper that attaches `cache_control: ephemeral` to the last tool and to the system prompt.

Rules of prompt caching this helper follows:
- Cache breakpoint goes on the last tool (covers all tools before it).
- Cache breakpoint goes on the system prompt (covers tools + system together).
- Max 4 breakpoints per request, min 1024 cached tokens to actually hit the cache.
- Anything before a breakpoint is cached; changing anything before invalidates the cache.
"""

from chat_tools import add_assistant_message, add_user_message
from chat_tools import chat as _chat


def _tag_last_tool(tools):
    if not tools:
        return None
    out = list(tools)
    out[-1] = {**out[-1], "cache_control": {"type": "ephemeral"}}
    return out


def _tag_system(system):
    if not system:
        return None
    if isinstance(system, str):
        return [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
    out = list(system)
    out[-1] = {**out[-1], "cache_control": {"type": "ephemeral"}}
    return out


def chat(messages, system=None, tools=None, **kwargs):
    """Chat with automatic cache_control on the last tool and on the system prompt."""
    return _chat(messages, system=_tag_system(system), tools=_tag_last_tool(tools), **kwargs)


__all__ = ["chat", "add_user_message", "add_assistant_message"]
