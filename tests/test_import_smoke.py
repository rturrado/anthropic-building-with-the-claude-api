"""Smoke-test imports of every top-level project module.

A broken import (missing dep, bad path, circular import) stays hidden until someone runs the affected notebook.
This test catches it in CI without running any code that calls the API.
"""

import importlib

import pytest

MODULES = [
    "chat",
    "chat_cache",
    "chat_tools",
    "files_api",
    "models",
    "tool_schemas",
]


@pytest.mark.parametrize("module_name", MODULES)
def test_module_imports(module_name: str) -> None:
    importlib.import_module(module_name)
