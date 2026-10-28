import anyio
import httpx2

from mcp import Client
from mcp.client.streamable_http import streamable_http_client

async def main() -> None:
    async with httpx2.AsyncClient(
        headers={
            "Authorization": "Bearer travel-dev-token",
        }
    ) as http_client:
        transport = streamable_http_client(
            "http://127.0.0.1:8000/mcp",
            http_client=http_client,
        )
        async with Client(transport) as client:
            # Discover available tools
            tools = await client.list_tools()

            print("=== Available Tools ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call an existing tool over HTTP
            result = await client.call_tool(
                "search_destinations",
                {
                    "city": "Bali",
                    "max_budget": 150000,
                },
            )

            print("\n=== Search Results ===")
            print(result.structured_content)


if __name__ == "__main__":
    anyio.run(main)
