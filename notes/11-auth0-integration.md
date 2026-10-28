# Auth0 Integration

## Overview

The `travel-mcp` project uses Auth0 to authenticate machine-to-machine clients connecting to the MCP server over Streamable HTTP.

The client obtains an access token from Auth0 using the OAuth 2.0 Client Credentials flow. It then sends the token to the MCP server using the HTTP Bearer authentication scheme.

## Architecture

1. The client loads its Auth0 configuration from environment variables.
2. The client requests an access token from the Auth0 token endpoint.
3. The client sends the access token in the `Authorization: Bearer` header.
4. The MCP server retrieves the signing key from the Auth0 JWKS endpoint.
5. The server validates the JWT signature, issuer, audience, expiration, and required scope.
6. The server accepts or rejects the request based on token validation.

## Configuration

Configure the following environment variables in the local `.env` file:

- `AUTH0_DOMAIN`
- `AUTH0_CLIENT_ID`
- `AUTH0_CLIENT_SECRET`
- `AUTH0_AUDIENCE`

Never commit `.env` or expose client secrets and access tokens.

## Authorization

The MCP server requires the `travel:read` scope.

The access token must have a valid signature and satisfy the configured issuer, audience, and expiration checks. Requests without a valid token must be rejected.

## Verification

The authentication flow was tested with the following scenarios:

- Valid Auth0 access token: accepted.
- Invalid access token: rejected.
- Missing access token: rejected.
- Existing automated tests: passed.

## Token Lifecycle

The client currently requests an access token when `client_http.py` starts. The token is reused for requests made by that client process.

Token caching and automatic renewal can be added as a future improvement.

## Limitations

This setup is intended for learning and local development. Production deployments should also consider HTTPS, secret management, key retrieval behavior, token caching, and operational monitoring.
