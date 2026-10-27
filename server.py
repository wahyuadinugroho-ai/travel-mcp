from mcp.server import MCPServer
from typing import TypedDict


mcp = MCPServer("Travel Assistant")

class TripBudgetResult(TypedDict):
    days: int
    daily_budget: int
    transport_cost: int
    total_budget: int


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


@mcp.tool()
def calculate_trip_budget(
    days: int,
    daily_budget: int,
    transport_cost: int,
) -> TripBudgetResult:
    """Calculate the estimated total budget for a trip."""
    return {
        "days": days,
        "daily_budget": daily_budget,
        "transport_cost": transport_cost,
        "total_budget": (days * daily_budget) + transport_cost,
    }


@mcp.resource("travel://destinations")
def get_destinations() -> list[dict]:
    """Return all available travel destinations."""
    return DESTINATIONS


@mcp.prompt()
def plan_trip(
    city: str,
    budget: int,
    days: int,
) -> str:
    """Create a travel planning prompt for a destination."""
    return (
        f"Create a {days}-day travel plan for {city}.\n"
        f"Total budget: IDR {budget:,}.\n"
        "Suggest an itinerary, estimated costs, and practical travel tips."
    )


if __name__ == "__main__":
    mcp.run()