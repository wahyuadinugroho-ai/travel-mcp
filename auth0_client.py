
import asyncio
import os
import time
import httpx2
from dotenv import load_dotenv


load_dotenv()

_cached_access_token: str | None = None
_token_expires_at = 0.0

async def get_access_token() -> str:
    global _cached_access_token, _token_expires_at

    # Reuse the cached token if it is still valid.
    if (
        _cached_access_token is not None
        and time.monotonic() < _token_expires_at - 60
    ):
        return _cached_access_token

    domain = os.environ["AUTH0_DOMAIN"].removeprefix("https://").rstrip("/")
    client_id = os.environ["AUTH0_CLIENT_ID"]
    client_secret = os.environ["AUTH0_CLIENT_SECRET"]
    audience = os.environ["AUTH0_AUDIENCE"]

    for attempt in range(3):
        try:
            async with httpx2.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"https://{domain}/oauth/token",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "audience": audience,
                        "scope": "travel:read",
                    },
                )
                response.raise_for_status()
                payload = response.json()
                break

        except httpx2.HTTPStatusError as exc:
            # Retry only for temporary server errors.
            if exc.response.status_code < 500 or attempt == 2:
                raise

        except httpx2.TransportError:
            # Retry network errors, but stop after the final attempt.
            if attempt == 2:
                raise

        await asyncio.sleep(2 ** attempt)

    _cached_access_token = payload["access_token"]
    _token_expires_at = time.monotonic() + payload["expires_in"]

    return _cached_access_token
