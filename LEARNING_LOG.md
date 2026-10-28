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

## 2026-10-28 — Error Handling and Retry Strategy (Lesson 13)

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

### Next Steps
- Complete Lesson 13 documentation and commit the milestone.
- Continue MCP foundations with Lesson 14.
- Evaluate additional hardening scenarios, including timeout retries and HTTP 429 handling.
- Complete the planned MCP foundations before introducing the LLM agent.

## Long-Term Project Goals

- Develop `travel-mcp` into a production-oriented Travel AI application with real data, an LLM agent, testing, and deployment.
- Develop `minimal-mcp` as a reusable MCP core for multiple domains.
- Keep learning notes separate from official project documentation.
- Refactor the application into a modular `src/` package when the appropriate milestone is reached.
