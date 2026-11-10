"""Compile every notebook's code cells without running them.

Cells are concatenated, run through IPython's input transformer to desugar line magics and shell
escapes, and handed to Python's builtin `compile`. This catches syntax errors and unknown magic
patterns in CI without touching the Anthropic API.
"""

import ast
import json
from pathlib import Path

import pytest
from IPython.core.inputtransformer2 import TransformerManager

ROOT = Path(__file__).parent.parent
EXCLUDED_PARTS = {".venv", ".ipynb_checkpoints"}
NOTEBOOKS = sorted(p for p in ROOT.rglob("*.ipynb") if EXCLUDED_PARTS.isdisjoint(p.parts))


def _concatenated_code(nb_path: Path) -> str:
    notebook = json.loads(nb_path.read_text())
    sources: list[str] = []
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = cell["source"]
        sources.append("".join(source) if isinstance(source, list) else source)
    return "\n\n".join(sources)


@pytest.mark.parametrize("nb_path", NOTEBOOKS, ids=lambda p: str(p.relative_to(ROOT)))
def test_notebook_compiles(nb_path: Path) -> None:
    transformed = TransformerManager().transform_cell(_concatenated_code(nb_path))
    compile(transformed, str(nb_path), "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
