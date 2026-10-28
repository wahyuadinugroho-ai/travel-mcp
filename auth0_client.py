
import os

import httpx2
from dotenv import load_dotenv


load_dotenv()


async def get_access_token() -> str:
    domain = os.environ["AUTH0_DOMAIN"].removeprefix("https://").rstrip("/")
    client_id = os.environ["AUTH0_CLIENT_ID"]
    client_secret = os.environ["AUTH0_CLIENT_SECRET"]
    audience = os.environ["AUTH0_AUDIENCE"]

    async with httpx2.AsyncClient() as client:
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

    return payload["access_token"]
