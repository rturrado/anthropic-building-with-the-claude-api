"""Test the cache_control tagging helpers in `chat_cache`.

Both helpers are pure functions, so no Anthropic client is mocked. The tests check that the last
tool and the last system block pick up `cache_control: ephemeral`, that falsy inputs round-trip
to None, and that the inputs are not mutated in place.
"""

from chat_cache import _tag_last_tool, _tag_system

_EPHEMERAL = {"type": "ephemeral"}


def test_tag_last_tool_returns_none_for_none() -> None:
    assert _tag_last_tool(None) is None


def test_tag_last_tool_returns_none_for_empty_list() -> None:
    assert _tag_last_tool([]) is None


def test_tag_last_tool_marks_only_the_last() -> None:
    tools = [{"name": "a"}, {"name": "b"}, {"name": "c"}]
    tagged = _tag_last_tool(tools)
    assert tagged == [
        {"name": "a"},
        {"name": "b"},
        {"name": "c", "cache_control": _EPHEMERAL},
    ]


def test_tag_last_tool_does_not_mutate_input() -> None:
    tools = [{"name": "a"}, {"name": "b"}]
    _tag_last_tool(tools)
    assert tools == [{"name": "a"}, {"name": "b"}]


def test_tag_system_returns_none_for_empty_string() -> None:
    assert _tag_system("") is None


def test_tag_system_returns_none_for_none() -> None:
    assert _tag_system(None) is None


def test_tag_system_wraps_plain_string() -> None:
    assert _tag_system("You are helpful.") == [
        {"type": "text", "text": "You are helpful.", "cache_control": _EPHEMERAL},
    ]


def test_tag_system_marks_only_the_last_block() -> None:
    system = [
        {"type": "text", "text": "a"},
        {"type": "text", "text": "b"},
    ]
    tagged = _tag_system(system)
    assert tagged == [
        {"type": "text", "text": "a"},
        {"type": "text", "text": "b", "cache_control": _EPHEMERAL},
    ]


def test_tag_system_does_not_mutate_input_list() -> None:
    system = [{"type": "text", "text": "a"}, {"type": "text", "text": "b"}]
    _tag_system(system)
    assert system == [{"type": "text", "text": "a"}, {"type": "text", "text": "b"}]
