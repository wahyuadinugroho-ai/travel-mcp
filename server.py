from mcp.server import MCPServer
from typing import TypedDict
from pydantic import AnyHttpUrl
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
import logging

logger = logging.getLogger(__name__)

RESOURCE_URL = "http://127.0.0.1:8000/mcp"

KNOWN_TOKENS = {
    "travel-dev-token": AccessToken(
        token="travel-dev-token",
        client_id="travel-local-client",
        scopes=["travel:read"],
        resource=RESOURCE_URL,
    )
}

class StaticTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        return KNOWN_TOKENS.get(token)

mcp = MCPServer(
    "Travel Assistant",
    token_verifier=StaticTokenVerifier(),
    auth=AuthSettings(
            issuer_url=AnyHttpUrl("https://auth.example.com"),
            resource_server_url=AnyHttpUrl(RESOURCE_URL),
            required_scopes=["travel:read"],
            validate_token_resource=True,
        ),
    )

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

    if not city.strip():
        raise ValueError("City cannot be empty.")

    if max_budget < 0:
        raise ValueError("Maximum budget cannot be negative.")

    logger.info("Searching destinations for city: %s", city)

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

    if days <= 0:
        raise ValueError("Days must be greater than zero.")

    if daily_budget < 0:
        raise ValueError("Daily budget cannot be negative.")

    if transport_cost < 0:
        raise ValueError("Transport cost cannot be negative.")
    
    logger.info("Calculating trip budget for %s days", days)

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