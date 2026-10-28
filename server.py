from dotenv import load_dotenv
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientConnectionError
from mcp.server import MCPServer
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from typing import TypedDict
import httpx
import jwt
import logging
import os

logger = logging.getLogger(__name__)

load_dotenv()

AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"].removeprefix("https://").rstrip("/")
AUTH0_AUDIENCE = os.environ["AUTH0_AUDIENCE"]
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_JWKS_URL = f"{AUTH0_ISSUER}.well-known/jwks.json"
RESOURCE_URL = "http://127.0.0.1:8000/mcp"

# KNOWN_TOKENS = {
#     "travel-dev-token": AccessToken(
#         token="travel-dev-token",
#         client_id="travel-local-client",
#         scopes=["travel:read"],
#         resource=RESOURCE_URL,
#     )
# }

# class StaticTokenVerifier(TokenVerifier):
#     async def verify_token(self, token: str) -> AccessToken | None:
#         return KNOWN_TOKENS.get(token)

class Auth0TokenVerifier(TokenVerifier):
    def __init__(self) -> None:
        self.jwks_client = PyJWKClient(AUTH0_JWKS_URL)

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=AUTH0_AUDIENCE,
                issuer=AUTH0_ISSUER,
                options={"require": ["exp", "iss", "aud"]},
            )

            scopes = claims.get("scope", "").split()
            if "travel:read" not in scopes:
                return None

            client_id = claims.get("azp") or claims.get("client_id")
            if not client_id:
                return None

            return AccessToken(
                token=token,
                client_id=client_id,
                scopes=scopes,
                expires_at=claims["exp"],
            )

        except PyJWKClientConnectionError:
            logger.warning("Unable to retrieve Auth0 signing keys.")
            return None

        except jwt.PyJWTError:
            logger.warning("JWT verification failed.")
            return None

mcp = MCPServer(
    "Travel Assistant",
    token_verifier=Auth0TokenVerifier(),
    auth=AuthSettings(
            issuer_url=AnyHttpUrl(AUTH0_ISSUER),
            resource_server_url=AnyHttpUrl(RESOURCE_URL),
            required_scopes=["travel:read"],
            validate_token_resource=False,
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


async def search_city(city: str) -> bool:
    """Check whether a city exists using the Open-Meteo Geocoding API."""

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPError:
        logger.warning("Open-Meteo geocoding request failed.")
        raise

    return bool(data.get("results"))

@mcp.tool()
async def search_destinations(
    city: str,
    max_budget: int,
) -> list[dict]:
    """Search travel destinations by city and maximum budget."""

    if not isinstance(city, str) or not city.strip():
        raise ValueError("City cannot be empty.")

    if len(city) > 100:
        raise ValueError("City cannot exceed 100 characters.")

    if isinstance(max_budget, bool) or not isinstance(max_budget, int):
        raise ValueError("Maximum budget must be an integer.")

    if max_budget < 0:
        raise ValueError("Maximum budget cannot be negative.")

    city = city.strip()

    logger.info("Searching destinations for city: %s", city)

    city_exists = await search_city(city)

    if not city_exists:
        return []

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

    if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
        raise ValueError("Days must be a positive integer.")

    if (
        isinstance(daily_budget, bool)
        or not isinstance(daily_budget, int)
        or daily_budget < 0
    ):
        raise ValueError("Daily budget must be a non-negative integer.")

    if (
        isinstance(transport_cost, bool)
        or not isinstance(transport_cost, int)
        or transport_cost < 0
    ):
        raise ValueError("Transport cost must be a non-negative integer.")
    
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