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

        # Calculate a trip budget
        budget_result = await client.call_tool(
            "calculate_trip_budget",
            {
                "days": 3,
                "daily_budget": 500000,
                "transport_cost": 300000,
            },
        )

        print("\n=== Trip Budget ===")

        if budget_result.is_error:
            print("The budget calculation failed.")
            for content in budget_result.content:
                if hasattr(content, "text"):
                    print(content.text)
        else:
            print(budget_result.structured_content)

        # Read the destinations resource
        resource_result = await client.read_resource(
            "travel://destinations"
        )

        print("\n=== All Destinations ===")
        for content in resource_result.contents:
            if isinstance(content, TextResourceContents):
                print(content.text)
        
        # List available prompts
        prompt_result = await client.list_prompts()

        print("\n=== Available Prompts ===")
        for prompt in prompt_result.prompts:
            print(f"- {prompt.name}: {prompt.description}")

        # Render the travel planning prompt
        rendered_prompt = await client.get_prompt(
            "plan_trip",
            {
                "city": "Bali",
                "budget": "1500000",
                "days": "3",
            },
        )

        print("\n=== Rendered Prompt ===")
        for message in rendered_prompt.messages:
            print(message.content.text)


if __name__ == "__main__":
    import anyio

    anyio.run(main)
