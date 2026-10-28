
import anyio

from mcp import Client


async def main() -> None:
    async with Client("http://0.0.0.0:8000/mcp") as client:
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
