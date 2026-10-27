import asyncio
import json

from mcp import Client, StdioServerParameters


server = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def main():
    async with Client(server) as client:
        tools = await client.list_tools()

        print("=== TOOLS TERSEDIA ===")
        for tool in tools.tools:
            print(f"- {tool.name}: {tool.description}")

        result = await client.call_tool(
            "search_destinations",
            {
                "city": "Bali",
                "max_budget": 150000,
            },
        )

        print("\n=== HASIL PENCARIAN ===")

        if result.is_error:
            print("Tool gagal dijalankan.")
            return

        # Ambil data terstruktur dari hasil MCP
        destinations = result.structured_content["result"]

        for index, destination in enumerate(destinations, start=1):
            print(f"\nDestinasi {index}")
            print(f"Nama   : {destination['name']}")
            print(f"Kota   : {destination['city']}")
            print(f"Budget : Rp{destination['budget']:,}".replace(",", "."))


if __name__ == "__main__":
    asyncio.run(main())