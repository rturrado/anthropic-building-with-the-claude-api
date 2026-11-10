"""Shared test fixtures for the Building with the Claude API test suite."""

import os

# Top-level modules create `Anthropic()` at import time, which requires ANTHROPIC_API_KEY to exist in the environment.
# In CI (and for contributors without a local .env), fill in a dummy value - the SDK only validates it when an actual
# API call is made, which these tests never do.
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-dummy-for-import-tests")
