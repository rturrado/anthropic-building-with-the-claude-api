# Building with the Claude API - parallel exercises

Side project I run in parallel to the free [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api) course from Anthropic Academy.
One folder per chapter at the project root, all sharing the same helper modules
(`chat.py`, `chat_tools.py`, `chat_cache.py`, `files_api.py`, `models.py`, `tool_schemas.py`)
and the same dependencies.

## Setup

1.  `uv sync`
2.  `cp .env.example .env`
3.  Edit `.env` and set your real `ANTHROPIC_API_KEY` and `VOYAGE_API_KEY`.
    See [Getting the keys](#getting-the-keys) for details.
    `VOYAGE_API_KEY` is only required for chapter 5 (RAG embeddings); the rest of the chapters run with `ANTHROPIC_API_KEY` alone.

### Getting the keys

#### `ANTHROPIC_API_KEY`

1.  Log in to the [Anthropic Console](https://console.anthropic.com).
2.  Go to *Settings / API Keys* and click *Create Key*.
3.  Give it a name and copy the key; it is shown only once.

New accounts get a small free credit.
Once it runs out, requests fail with `429` until you top up or enable billing on the workspace.

#### `VOYAGE_API_KEY`

1.  Sign up at [VoyageAI](https://www.voyageai.com) and go to the API keys dashboard.
2.  Create a key and copy it.

Chapter 5 uses `voyage-3-large` for embeddings; the free tier is enough to run the notebook end to end.

## Running a chapter

Each chapter is a folder of Jupyter notebooks. Open any `.ipynb` with Jupyter or your IDE.
From the command line:

```
uv run jupyter notebook 1-accessing-claude-with-the-api/
```

Change the path to the chapter you want to run.

## Chapters

1.  Accessing Claude with the API
2.  Prompt evaluation
3.  Prompt engineering
4.  Tool use
5.  Retrieval-augmented generation
6.  Features of Claude (thinking, images, PDF, citations, caching, code execution + files)
7.  Model Context Protocol — interactive CLI app, see [`7-model-context-protocol/README.md`](7-model-context-protocol/README.md).
