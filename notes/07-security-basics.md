# MCP Security Basics

## Objective

Understand the basic security considerations for MCP servers.

## Local Server Binding

The HTTP server binds to `127.0.0.1`, making it accessible through the local loopback interface rather than listening on all network interfaces.

Keep this configuration for local development.

## Input Validation

Validate tool arguments before processing requests.

The current server validates destination search inputs and trip budget calculations.

## Secrets Management

- Never commit access tokens, API keys, passwords, or private credentials.
- Store real secrets outside source code.
- Keep `.env` files out of Git.
- Provide `.env.example` only for documenting variable names and non-secret placeholders.

## Authentication

Authentication verifies the identity or credentials of a client.

For protected Streamable HTTP deployments, use a supported authentication design based on the MCP authorization specification and OAuth 2.1. Do not treat a custom tool argument or an unverified token as authentication.

## Security Checklist

- [ ] Keep local development servers bound to localhost.
- [ ] Validate tool inputs.
- [ ] Handle errors without exposing secrets.
- [ ] Keep credentials out of source code and Git.
- [ ] Understand the authorization requirements before exposing the server to a network.
- [ ] Verify access tokens and required scopes when implementing authorization.

## References

- [https://py.sdk.modelcontextprotocol.io/run/authorization/](https://py.sdk.modelcontextprotocol.io/run/authorization/)
- [https://py.sdk.modelcontextprotocol.io/run/deploy/](https://py.sdk.modelcontextprotocol.io/run/deploy/)
- [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
