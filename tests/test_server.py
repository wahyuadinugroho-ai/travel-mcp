
import pytest
from mcp import Client

from server import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as connected_client:
        yield connected_client


@pytest.mark.anyio
async def test_search_destinations(client):
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
