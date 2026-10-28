
# Authentication

## Overview

The HTTP transport uses bearer-token authentication through the MCP SDK's token verifier.

This implementation uses a static token for local learning purposes. It is not a complete OAuth implementation and must not be used in production.

## Configuration

- Transport: Streamable HTTP
- Endpoint: `http://127.0.0.1:8000/mcp`
- Required scope: `travel:read`
- Token resource validation: enabled

## Local Development

Start the HTTP server:

```bash
uv run server_http.py
```

Run the HTTP client in another terminal:

```bash
uv run client_http.py
```

The client sends a bearer token in its Authorization header.

## Verification

Test the following scenarios:

1. A valid token allows the client to access the server.
2. An invalid token is rejected.
3. A missing token is rejected.

The existing in-memory tests verify application functionality separately from HTTP authentication.

## Security Limitations

- The token is hardcoded for local development.
- The token is not issued by a real authorization server.
- The issuer URL is placeholder metadata.
- Do not commit real credentials or use this configuration in production.

A production deployment should use a proper OAuth authorization server, secure token validation, HTTPS, and appropriate secret management.
