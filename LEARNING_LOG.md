# Learning Log

## 2026-10-27 — MCP Fundamentals (Lessons 1–10)

### Objectives
- Understand MCP fundamentals using the MCP Python SDK.
- Build an MCP server and client using `uv`.
- Learn MCP tools, resources, and prompts.
- Test MCP capabilities using MCP Inspector.

### What I Built
- An MCP server named `Travel Assistant`.
- A `search_destinations` tool.
- A `calculate_trip_budget` tool.
- A Python MCP client.
- A destinations resource and a trip-planning prompt.

### What I Learned
- MCP is a protocol, not an LLM or an AI agent.
- MCP servers expose capabilities through tools, resources, and prompts.
- MCP clients can discover and invoke server capabilities programmatically.
- Tools can be used without an LLM.
- `uv` manages Python dependencies and project execution.

### Challenges
- The initial project name conflicted with the third-party package name `mcp`.
- The project was renamed to `travel-mcp`.

## 2026-10-28 — HTTP Transport and Auth0 Authentication (Lessons 11–12)

### Objectives
- Expose the MCP server over Streamable HTTP.
- Implement Auth0 authentication.
- Obtain and cache access tokens using the client credentials flow.
- Protect the MCP server with token validation and scope checks.

### What I Built
- An HTTP MCP server and client.
- An Auth0 token verifier.
- An Auth0 client credentials flow.
- Access-token caching with expiration handling.
- Automated tests for token caching and token refresh.

### What I Learned
- Streamable HTTP allows MCP communication over HTTP.
- OAuth 2.0 client credentials can authenticate machine-to-machine clients.
- Access tokens must be validated by the resource server.
- Token caching reduces unnecessary requests to the identity provider.
- Cached tokens should be refreshed before expiration.

### Testing
- Verified successful token acquisition.
- Verified token reuse while the cached token remains valid.
- Verified refresh when the token approaches expiration.
- Verified authentication failures are rejected.

## Lesson 13 — Error Handling and Retry Strategy

### Objectives
- Add request timeouts to Auth0 token requests.
- Implement retries for temporary server and network errors.
- Verify retry behavior with automated tests.

### What I Built
- A 10-second timeout for Auth0 token requests.
- A maximum of three attempts for retryable failures.
- Exponential backoff delays of 1 and 2 seconds.
- Automated tests for HTTP 500 recovery, HTTP 401 handling, and network errors.

### What I Learned
- Timeouts prevent requests from waiting indefinitely.
- Retries can recover from temporary network and server failures.
- HTTP 4xx errors should not be retried indiscriminately.
- Exponential backoff spaces out repeated attempts.
- Mock transports and mocked sleep functions make retry tests deterministic.

### Testing
- Verified HTTP 500 responses can recover through retry.
- Verified HTTP 401 responses fail without retrying.
- Verified network errors are retried up to three attempts.
- Verified the existing token-caching tests still pass.
- Confirmed the test suite passes after the changes.

## Lesson 14 — Logging and Observability

- Added Python logging to the Auth0 token client.
- Added DEBUG, INFO, and WARNING logs for token caching, requests, retries, and failures.
- Added tests using pytest `caplog` to verify retry and cache logging.
- Verified that access tokens and client secrets are not exposed in the tested log output.
- Confirmed that all 11 tests pass.

## Lesson 15 — MCP Security Hardening

- Strengthened tool input validation.
- Rejected boolean values for integer inputs.
- Added explicit handling for JWT verification and JWKS connection failures.
- Added tests for authentication failure logging and token-string protection.
- Confirmed that all 15 tests pass.

## Lesson 16 — Public API Integration

### Goal
Integrate a public API into the existing Travel MCP server while preserving existing MCP tools, resources, prompts, and authentication.

### What I Learned
- Added `httpx` to make asynchronous HTTP requests.
- Integrated the Open-Meteo Geocoding API to check whether a city exists.
- Updated `search_destinations` to asynchronously validate a city before searching local destination data.
- Kept destination names and budget values in the existing local dataset.
- Added error handling for HTTP failures and logging without exposing sensitive information.
- Mocked API calls in tests to avoid relying on an external service during test execution.

### Testing
- Added a test for a city that is not found.
- Added a test for HTTP errors from the geocoding API.
- Verified that existing MCP and Auth0 tests continue to pass.
- Result: **17 tests passed**.

### Important Note
The Open-Meteo API validates city existence only. Destination names and budget values still come from the local `DESTINATIONS` dataset; they are not retrieved from the API.

### Next Steps
- Review the Lesson 16 changes.
- Commit the completed milestone.
- Continue with Lesson 17.

## Long-Term Project Goals

- Develop `travel-mcp` into a production-oriented Travel AI application with real data, an LLM agent, testing, and deployment.
- Develop `minimal-mcp` as a reusable MCP core for multiple domains.
- Keep learning notes separate from official project documentation.
- Refactor the application into a modular `src/` package when the appropriate milestone is reached.

## Next Steps

- Complete the Lesson 15 documentation and commit/push the milestone if not already done.
- Begin Lesson 16: integrate the MCP client with a real data source or external API.
- Continue the planned MCP foundations before introducing the LLM agent.
- Build toward the reusable `minimal-mcp` core and the end-to-end Travel AI application.
