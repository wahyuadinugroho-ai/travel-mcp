from mcp.server import MCPServer

mcp = MCPServer("Travel Assistant")

DESTINATIONS = [
    {
        "city": "Bali",
        "name": "Pantai Kuta",
        "budget": 100_000,
    },
    {
        "city": "Bali",
        "name": "Ubud",
        "budget": 250_000,
    },
    {
        "city": "Yogyakarta",
        "name": "Candi Prambanan",
        "budget": 150_000,
    },
    {
        "city": "Bandung",
        "name": "Kawah Putih",
        "budget": 200_000,
    },
]


@mcp.tool()
def search_destinations(
    city: str,
    max_budget: int,
) -> list[dict]:
    """Cari destinasi wisata berdasarkan kota dan budget maksimum."""

    results = [
        destination
        for destination in DESTINATIONS
        if destination["city"].lower() == city.lower()
        and destination["budget"] <= max_budget
    ]

    return results


@mcp.resource("travel://destinations")
def get_destinations() -> list[dict]:
    """Return all available travel destinations."""
    return DESTINATIONS


if __name__ == "__main__":
    mcp.run()