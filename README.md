# Travel MCP

A hands-on learning project exploring the Model Context Protocol (MCP) using Python and the official MCP Python SDK.

The goal is to understand MCP through practical implementations, technical documentation, automated testing, and incremental experiments.

## Learning Objectives

- Understand MCP architecture and core concepts.
- Build MCP servers and clients using Python.
- Implement tools, resources, and prompts.
- Explore MCP transport mechanisms.
- Implement input validation and error handling.
- Learn authentication, security, and observability.
- Write automated tests for MCP functionality.
- Prepare the application for external API integration and future deployment.

## Tech Stack

- Python 3.11+
- MCP Python SDK
- `uv` for dependency and project management
- Auth0 for machine-to-machine authentication
- PyJWT for JWT validation
- `httpx`-based HTTP requests
- pytest for automated testing
- Git and GitHub

## Current Implementation

### Travel Assistant MCP Server

The project currently includes an MCP server named `Travel Assistant`.

#### MCP Capabilities

- `search_destinations`: Search sample travel destinations by city and maximum budget.
- `calculate_trip_budget`: Calculate an estimated trip budget.
- `travel://destinations`: A resource for accessing destination data.
- `plan_trip`: A prompt for generating a trip-planning request.

The destination search currently uses in-memory sample data. Integration with a real travel API is a planned next step.

#### Client and Transport

- Python MCP client.
- Tool discovery and invocation.
- Resource and prompt access.
- Streamable HTTP transport.
- MCP Inspector testing.

#### Authentication and Security

- Auth0 client credentials flow.
- Access-token caching and expiration handling.
- JWT validation using Auth0 signing keys.
- Audience, issuer, expiration, and required-scope checks.
- Input validation for MCP tool arguments.
- Explicit handling of JWT verification and JWKS connection failures.

#### Reliability and Observability

- HTTP request timeouts for Auth0 token requests.
- Retries for retryable HTTP and network failures.
- Exponential backoff.
- Python logging at DEBUG, INFO, and WARNING levels.
- Automated tests for token caching, retries, logging, validation, and authentication failures.

## Example Tool Input

Example input for `search_destinations`:

```json
{
  "city": "Bali",
  "max_budget": 150000
}
```

The tool searches the configured sample destination data for destinations matching the city and budget.

For example, a matching sample destination could be Pantai Kuta with a budget of IDR 100,000. Actual results depend on the data currently defined in the project.

## Project Structure

```text
travel-mcp/
├── server.py
├── client.py
├── server_http.py
├── client_http.py
├── auth0_client.py
├── tests/
│   ├── test_server.py
│   └── test_auth0_client.py
├── notes/
│   ├── 01-...
│   ├── ...
│   └── 15-security-hardening.md
├── pyproject.toml
├── uv.lock
├── README.md
├── LEARNING_LOG.md
├── .gitignore
└── .env
```

The structure above summarizes the main files. Keep the actual filenames in this section synchronized with the repository as it evolves. The `.env` file contains local configuration and secrets and must not be committed.

## Running the Project

Install dependencies:

```bash
uv sync
```

Run the local MCP server:

```bash
uv run python server.py
```

Run the automated tests:

```bash
uv run pytest -v
```

For HTTP transport, use the configuration and startup instructions documented in the relevant project notes.

Authentication-dependent commands require valid local Auth0 configuration. Do not commit client secrets, access tokens, or other credentials.

## Learning Roadmap

### Completed

- [x] MCP server fundamentals
- [x] MCP client fundamentals
- [x] MCP tools, resources, and prompts
- [x] Streamable HTTP transport
- [x] Auth0 client credentials authentication
- [x] Access-token caching and expiration handling
- [x] Timeout, retry, and exponential backoff strategy
- [x] Logging and observability
- [x] Input validation and security hardening
- [x] Automated testing for core functionality

### Planned

- [ ] Integrate a real travel API.
- [ ] Separate external API clients and application services.
- [ ] Improve data modeling and structured outputs.
- [ ] Evaluate database integration where appropriate.
- [ ] Expand integration and failure-scenario tests.
- [ ] Introduce an LLM-powered travel agent.
- [ ] Build a user-facing Travel AI application.
- [ ] Prepare deployment and production-readiness workflows.
- [ ] Develop `minimal-mcp` as a reusable MCP core for other domains.

## Learning Approach

Each topic follows three steps:

1. Understand the concepts.
2. Implement a working example.
3. Document the implementation, test results, challenges, and lessons learned.

The project evolves incrementally. Existing functionality and tests should remain stable as new capabilities are introduced.

## References

- [MCP Python SDK Documentation](https://py.sdk.modelcontextprotocol.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Auth0 Documentation](https://auth0.com/docs/)
- [pytest Documentation](https://docs.pytest.org/)
