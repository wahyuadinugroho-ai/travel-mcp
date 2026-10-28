
import httpx2
import logging
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


@pytest.mark.anyio
async def test_get_access_token_retries_server_error(monkeypatch, caplog):
    caplog.set_level(logging.DEBUG, logger="auth0_client")

    request_count = 0

    def mock_handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1

        if request_count == 1:
            return httpx2.Response(500, json={"error": "server_error"})

        return httpx2.Response(
            200,
            json={
                "access_token": "recovered-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )

    monkeypatch.setenv("AUTH0_DOMAIN", "example.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("AUTH0_AUDIENCE", "https://travel-mcp-api")

    monkeypatch.setattr(auth0_client, "_cached_access_token", None)
    monkeypatch.setattr(auth0_client, "_token_expires_at", 0.0)

    async def mock_sleep(delay):
        pass

    monkeypatch.setattr(auth0_client.asyncio, "sleep", mock_sleep)

    transport = httpx2.MockTransport(mock_handler)
    original_async_client = httpx2.AsyncClient

    def mock_async_client(**kwargs):
        return original_async_client(transport=transport, **kwargs)

    monkeypatch.setattr(auth0_client.httpx2, "AsyncClient", mock_async_client)

    token = await auth0_client.get_access_token()

    assert token == "recovered-token"
    assert request_count == 2

    # Verify retry and success logs.
    assert "Auth0 returned HTTP 500 on attempt 1." in caplog.text
    assert "Successfully obtained an Auth0 access token." in caplog.text


@pytest.mark.anyio
async def test_get_access_token_does_not_retry_client_error(monkeypatch):
    request_count = 0

    def mock_handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1
        return httpx2.Response(401, json={"error": "unauthorized"})

    monkeypatch.setenv("AUTH0_DOMAIN", "example.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("AUTH0_AUDIENCE", "https://travel-mcp-api")

    monkeypatch.setattr(auth0_client, "_cached_access_token", None)
    monkeypatch.setattr(auth0_client, "_token_expires_at", 0.0)

    async def mock_sleep(delay):
        pass

    monkeypatch.setattr(auth0_client.asyncio, "sleep", mock_sleep)

    transport = httpx2.MockTransport(mock_handler)
    original_async_client = httpx2.AsyncClient

    def mock_async_client(**kwargs):
        return original_async_client(transport=transport, **kwargs)

    monkeypatch.setattr(auth0_client.httpx2, "AsyncClient", mock_async_client)

    with pytest.raises(httpx2.HTTPStatusError):
        await auth0_client.get_access_token()

    assert request_count == 1


@pytest.mark.anyio
async def test_get_access_token_retries_network_error(monkeypatch):
    request_count = 0

    def mock_handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1
        raise httpx2.ConnectError("network error", request=request)

    monkeypatch.setenv("AUTH0_DOMAIN", "example.auth0.com")
    monkeypatch.setenv("AUTH0_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("AUTH0_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv("AUTH0_AUDIENCE", "https://travel-mcp-api")

    monkeypatch.setattr(auth0_client, "_cached_access_token", None)
    monkeypatch.setattr(auth0_client, "_token_expires_at", 0.0)

    async def mock_sleep(delay):
        pass

    monkeypatch.setattr(auth0_client.asyncio, "sleep", mock_sleep)

    transport = httpx2.MockTransport(mock_handler)
    original_async_client = httpx2.AsyncClient

    def mock_async_client(**kwargs):
        return original_async_client(transport=transport, **kwargs)

    monkeypatch.setattr(auth0_client.httpx2, "AsyncClient", mock_async_client)

    with pytest.raises(httpx2.ConnectError):
        await auth0_client.get_access_token()

    assert request_count == 3


@pytest.mark.anyio
async def test_get_access_token_logs_cache_reuse_without_secrets(
    monkeypatch,
    caplog,
):
    import logging

    caplog.set_level(logging.DEBUG, logger="auth0_client")

    monkeypatch.setattr(
        auth0_client,
        "_cached_access_token",
        "test-access-token",
    )
    monkeypatch.setattr(
        auth0_client,
        "_token_expires_at",
        auth0_client.time.monotonic() + 3600,
    )

    token = await auth0_client.get_access_token()

    assert token == "test-access-token"
    assert "Reusing cached Auth0 access token." in caplog.text

    # Ensure logs do not expose credentials or access tokens.
    assert "test-client-secret" not in caplog.text
    assert "test-access-token" not in caplog.text
