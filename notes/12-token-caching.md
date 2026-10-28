# Token Caching and Expiration Handling

## Overview

The `travel-mcp` HTTP client caches its Auth0 access token in memory to avoid requesting a new token every time `get_access_token()` is called.

## Implementation

The token cache stores:

- `_cached_access_token`: the current access token.
- `_token_expires_at`: the token expiration deadline, measured with `time.monotonic()`.

The client reuses the cached token when more than 60 seconds remain before its expiration deadline. Otherwise, it requests a new token using the OAuth 2.0 Client Credentials flow.

## Testing

Automated tests verify that:

- A valid cached token is reused without another HTTP request.
- A token with only 30 seconds remaining is replaced with a new token.

The tests use a mock HTTP transport and do not contact Auth0.

## Limitations

The cache exists only in the current Python process. Restarting the client clears it.

This implementation is suitable for the current learning project. Production systems may need additional handling for concurrent token requests, network failures, and token endpoint errors.
