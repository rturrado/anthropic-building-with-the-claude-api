"""Entry point of the chapter 7 MCP chat demo.

Reads any extra server scripts from argv, constructs an `MCPClient` for the local `mcp_server.py`
(plus one per extra script), wires them to the `Claude` service and a `CliChat` + `CliApp`,
and starts the interactive chat loop.
"""

import asyncio
import os
import sys
from contextlib import AsyncExitStack

from core.claude import Claude
from core.cli import CliApp
from core.cli_chat import CliChat
from dotenv import load_dotenv
from mcp_client import MCPClient

from models import MODEL_HAIKU

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
assert anthropic_api_key, "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"

claude_model = MODEL_HAIKU


async def main():
    claude_service = Claude(model=claude_model)

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = "uv", ["run", "mcp_server.py"]

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(MCPClient(command=command, args=args))
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(MCPClient(command="uv", args=["run", server_script]))
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
