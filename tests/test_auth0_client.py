
import httpx2
import pytest

import auth0_client


@pytest.mark.anyio
async def test_get_access_token_reuses_cached_token(monkeypatch):
    request_count = 0

    def mock_handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1

        return httpx2.Response(
            200,
            json={
                "access_token": "test-access-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )

    # Configure test credentials.
    monkeypatch.setenv("AUTH0_DOMAIN", "example.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("AUTH0_AUDIENCE", "https://travel-mcp-api")

    # Reset the cache before testing.
    monkeypatch.setattr(auth0_client, "_cached_access_token", None)
    monkeypatch.setattr(auth0_client, "_token_expires_at", 0.0)

    # Route HTTP requests to the mock handler.
    transport = httpx2.MockTransport(mock_handler)
    original_async_client = httpx2.AsyncClient

    def mock_async_client(**kwargs):
        return original_async_client(
            transport=transport,
            **kwargs,
        )

    monkeypatch.setattr(
        auth0_client.httpx2,
        "AsyncClient",
        mock_async_client,
    )

    first_token = await auth0_client.get_access_token()
    second_token = await auth0_client.get_access_token()

    assert first_token == "test-access-token"
    assert second_token == first_token
    assert request_count == 1


@pytest.mark.anyio
async def test_get_access_token_refreshes_near_expiration(monkeypatch):
    request_count = 0

    def mock_handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1

        return httpx2.Response(
            200,
            json={
                "access_token": f"test-token-{request_count}",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )

    monkeypatch.setenv("AUTH0_DOMAIN", "example.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("AUTH0_AUDIENCE", "https://travel-mcp-api")

    monkeypatch.setattr(auth0_client, "_cached_access_token", "old-token")
    monkeypatch.setattr(
        auth0_client,
        "_token_expires_at",
        auth0_client.time.monotonic() + 30,
    )

    transport = httpx2.MockTransport(mock_handler)
    original_async_client = httpx2.AsyncClient

    def mock_async_client(**kwargs):
        return original_async_client(
            transport=transport,
            **kwargs,
        )

    monkeypatch.setattr(
        auth0_client.httpx2,
        "AsyncClient",
        mock_async_client,
    )

    token = await auth0_client.get_access_token()

    assert token == "test-token-1"
    assert request_count == 1
