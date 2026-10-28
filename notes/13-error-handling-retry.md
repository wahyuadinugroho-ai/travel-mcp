# Lesson 13 — Error Handling & Retry Strategy

## Objective

Improve the reliability of Auth0 access-token requests by adding request timeouts, retry handling, and automated tests.

## Implementation

### 1. Request Timeout

The Auth0 token request uses a 10-second timeout.

```python
async with httpx2.AsyncClient(timeout=10.0) as client:
```

This prevents requests from waiting indefinitely when Auth0 does not respond.

### 2. Retry Policy

The token request allows a maximum of three attempts.

| Error condition | Behavior |
|---|---|
| HTTP 5xx | Retry up to the maximum number of attempts |
| HTTP 4xx | Raise the error without retrying |
| Network transport error | Retry up to the maximum number of attempts |
| Successful response | Cache the access token and its expiration time |

Retry delays use exponential backoff:

- First retry: 1 second
- Second retry: 2 seconds

The retry delay is implemented using `asyncio.sleep()`.

### 3. Token Caching

The existing token cache remains in place. A cached token is reused while it is valid, with a 60-second safety margin before expiration.

When a new token is obtained successfully, the cache and expiration timestamp are updated.

## Automated Tests

The Auth0 client tests cover:

- Reusing a cached access token.
- Refreshing a token that is near expiration.
- Retrying after an HTTP 500 response.
- Avoiding retries after an HTTP 401 response.
- Retrying network errors up to three attempts.

Retry delays are mocked in tests to avoid unnecessary waiting.

## Verification

Run the Auth0 client tests:

```bash
uv run pytest tests/test_auth0_client.py -v
```

Run the complete test suite:

```bash
uv run pytest -v
```

All tests passed after implementing the timeout and retry strategy.

## Production Hardening Notes

The current implementation establishes basic retry behavior. Further hardening should evaluate:

- Retrying transient timeout errors.
- Handling HTTP 429 responses and `Retry-After`.
- Adding structured logging for retry attempts.
- Reviewing retry limits and backoff behavior.
- Avoiding retries for permanent authentication or configuration errors.

## Key Takeaways

- Timeouts limit how long an HTTP request can wait.
- Retries can recover from temporary network and server failures.
- Client errors should not be retried indiscriminately.
- Automated tests verify both successful recovery and expected failure behavior.
- Token caching and retry handling solve different problems and should remain independently testable.
