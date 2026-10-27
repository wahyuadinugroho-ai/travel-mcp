from mcp import Client, StdioServerParameters
from mcp.types import TextResourceContents


async def main() -> None:
    server = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
    )

    async with Client(server) as client:
        # List available tools
        tools = await client.list_tools()

        print("=== Available Tools ===")
        for tool in tools.tools:
            print(f"- {tool.name}: {tool.description}")

        # Call the existing search tool
        tool_result = await client.call_tool(
            "search_destinations",
            {
                "city": "Bali",
                "max_budget": 150000,
            },
        )

        print("\n=== Search Results ===")
        print(tool_result.structured_content)

        # Read the destinations resource
        resource_result = await client.read_resource(
            "travel://destinations"
        )

        print("\n=== All Destinations ===")
        for content in resource_result.contents:
            if isinstance(content, TextResourceContents):
                print(content.text)


if __name__ == "__main__":
    import anyio

    anyio.run(main)
