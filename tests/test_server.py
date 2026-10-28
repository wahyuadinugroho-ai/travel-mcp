import httpx
import jwt
import logging
import pytest
from jwt.exceptions import PyJWKClientConnectionError
from mcp import Client
from server import Auth0TokenVerifier, mcp
from unittest.mock import patch


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as connected_client:
        yield connected_client


@pytest.mark.anyio
async def test_search_destinations(client, monkeypatch):
    async def mock_search_city(city: str) -> bool:
        return True

    monkeypatch.setattr("server.search_city", mock_search_city)

    result = await client.call_tool(
        "search_destinations",
        {
            "city": "Bali",
            "max_budget": 150000,
        },
    )

    assert not result.is_error
    assert "Pantai Kuta" in str(result.structured_content)


@pytest.mark.anyio
async def test_search_destinations_returns_empty_when_city_not_found(
    client, monkeypatch
):
    async def mock_search_city(city: str) -> bool:
        return False

    monkeypatch.setattr("server.search_city", mock_search_city)

    result = await client.call_tool(
        "search_destinations",
        {
            "city": "KotaFiktifXYZ",
            "max_budget": 500_000,
        },
    )

    assert not result.is_error
    assert result.structured_content == {"result": []}


@pytest.mark.anyio
async def test_calculate_trip_budget(client):
    result = await client.call_tool(
        "calculate_trip_budget",
        {
            "days": 3,
            "daily_budget": 500000,
            "transport_cost": 300000,
        },
    )

    assert not result.is_error
    assert "1800000" in str(result.structured_content)


@pytest.mark.anyio
async def test_reject_invalid_trip_duration(client):
    result = await client.call_tool(
        "calculate_trip_budget",
        {
            "days": 0,
            "daily_budget": 500000,
            "transport_cost": 300000,
        },
    )

    assert result.is_error


@pytest.mark.anyio
async def test_destinations_resource(client):
    result = await client.read_resource(
        "travel://destinations"
    )

    assert result.contents
    assert "Bali" in str(result.contents)


@pytest.mark.anyio
async def test_plan_trip_prompt(client):
    result = await client.get_prompt(
        "plan_trip",
        {
            "city": "Bali",
            "budget": "1500000",
            "days": "3",
        },
    )

    assert result.messages
    assert "Bali" in str(result.messages)


@pytest.mark.anyio
async def test_search_destinations_rejects_excessively_long_city():
    from server import search_destinations

    with pytest.raises(ValueError):
        await search_destinations("A" * 101, 500_000)


def test_calculate_trip_budget_rejects_boolean_days():
    from server import calculate_trip_budget

    with pytest.raises(ValueError):
        calculate_trip_budget(True, 100_000, 50_000)


@pytest.mark.anyio
async def test_auth0_verifier_rejects_invalid_token(caplog):
    caplog.set_level(logging.WARNING, logger="server")

    verifier = Auth0TokenVerifier()

    with patch.object(
        verifier.jwks_client,
        "get_signing_key_from_jwt",
        side_effect=jwt.InvalidTokenError("invalid token"),
    ):
        result = await verifier.verify_token("invalid-token")

    assert result is None
    assert "JWT verification failed." in caplog.text
    assert "invalid-token" not in caplog.text


@pytest.mark.anyio
async def test_auth0_verifier_handles_jwks_connection_error(caplog):
    caplog.set_level(logging.WARNING, logger="server")

    verifier = Auth0TokenVerifier()

    with patch.object(
        verifier.jwks_client,
        "get_signing_key_from_jwt",
        side_effect=PyJWKClientConnectionError("connection failed"),
    ):
        result = await verifier.verify_token("test-token")

    assert result is None
    assert "Unable to retrieve Auth0 signing keys." in caplog.text
    assert "test-token" not in caplog.text


@pytest.mark.anyio
async def test_search_city_raises_on_http_error(monkeypatch):
    from server import search_city

    class MockResponse:
        def raise_for_status(self):
            raise httpx.HTTPStatusError(
                "Server error",
                request=httpx.Request("GET", "https://example.com"),
                response=httpx.Response(500),
            )

        def json(self):
            return {}

    class MockClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, *args, **kwargs):
            return MockResponse()

    monkeypatch.setattr("server.httpx.AsyncClient", MockClient)

    with pytest.raises(httpx.HTTPStatusError):
        await search_city("Jakarta")


@pytest.mark.anyio
async def test_search_tourist_places(monkeypatch):
    from server import search_tourist_places

    monkeypatch.setenv("GEOAPIFY_API_KEY", "test-api-key")

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "features": [
                    {
                        "properties": {
                            "name": "Pura Dalem Cemara",
                            "lat": -8.7229,
                            "lon": 115.2368,
                            "categories": ["tourism", "tourism.sights"],
                        }
                    },
                    {
                        "properties": {
                            "name": None,
                            "lat": -8.65,
                            "lon": 115.21,
                            "categories": ["tourism"],
                        }
                    },
                ]
            }

    class MockClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def get(self, url, params):
            assert url == "https://api.geoapify.com/v2/places"
            assert params["categories"] == "tourism.attraction,tourism.sights"
            return MockResponse()

    monkeypatch.setattr("server.httpx.AsyncClient", MockClient)

    result = await search_tourist_places(
        latitude=-8.6705,
        longitude=115.2126,
        radius_meters=5000,
    )

    assert len(result) == 1
    assert result[0]["name"] == "Pura Dalem Cemara"
    assert result[0]["lat"] == -8.7229
    assert result[0]["lon"] == 115.2368


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("latitude", "longitude", "radius_meters"),
    [
        (91, 115.2, 5000),
        (-91, 115.2, 5000),
        (-8.67, 181, 5000),
        (-8.67, -181, 5000),
        (-8.67, 115.2, 0),
        (-8.67, 115.2, 20001),
        (True, 115.2, 5000),
        (-8.67, 115.2, True),
    ],
)
async def test_search_tourist_places_rejects_invalid_input(
    monkeypatch,
    latitude,
    longitude,
    radius_meters,
):
    from server import search_tourist_places

    monkeypatch.setenv("GEOAPIFY_API_KEY", "test-api-key")

    with pytest.raises(ValueError):
        await search_tourist_places(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
        )


@pytest.mark.anyio
async def test_search_tourist_places_raises_on_http_error(monkeypatch):
    from server import search_tourist_places

    monkeypatch.setenv("GEOAPIFY_API_KEY", "test-api-key")

    class MockResponse:
        def raise_for_status(self):
            raise httpx.HTTPStatusError(
                "Server error",
                request=httpx.Request(
                    "GET",
                    "https://api.geoapify.com/v2/places",
                ),
                response=httpx.Response(500),
            )

    class MockClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def get(self, url, params):
            return MockResponse()

    monkeypatch.setattr("server.httpx.AsyncClient", MockClient)

    with pytest.raises(httpx.HTTPStatusError):
        await search_tourist_places(
            latitude=-8.6705,
            longitude=115.2126,
            radius_meters=5000,
        )


@pytest.mark.anyio
async def test_search_tourist_places_is_registered(client):
    result = await client.list_tools()

    tool_names = [tool.name for tool in result.tools]

    assert "search_tourist_places" in tool_names


@pytest.mark.anyio
async def test_search_tourist_places_through_mcp_client(client, monkeypatch):
    monkeypatch.setenv("GEOAPIFY_API_KEY", "test-api-key")

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "features": [
                    {
                        "properties": {
                            "name": "Pura Dalem Cemara",
                            "lat": -8.7229,
                            "lon": 115.2368,
                            "categories": ["tourism.sights"],
                        }
                    }
                ]
            }

    class MockClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def get(self, url, params):
            assert url == "https://api.geoapify.com/v2/places"
            return MockResponse()

    monkeypatch.setattr("server.httpx.AsyncClient", MockClient)

    result = await client.call_tool(
        "search_tourist_places",
        {
            "latitude": -8.6705,
            "longitude": 115.2126,
            "radius_meters": 5000,
        },
    )

    assert not result.is_error
    assert any(
        "Pura Dalem Cemara" in item.text
        for item in result.content
        if hasattr(item, "text")
    )
