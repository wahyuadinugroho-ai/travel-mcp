# MCP Transport Mechanisms

## Objective

Understand the difference between stdio and Streamable HTTP transports in the MCP Python SDK v2.

## stdio

The stdio transport allows a client to communicate with a server process through standard input and standard output.

It is useful for local integrations where the client launches the server process.

## Streamable HTTP

Streamable HTTP allows a client to communicate with an MCP server through an HTTP endpoint.

In this project, the server listens on `127.0.0.1:8000` and exposes the MCP endpoint at `/mcp`.

## Implementation

- `server.py` retains the original stdio configuration.
- `server_http.py` runs the existing MCP server over Streamable HTTP.
- `client.py` retains the original stdio client.
- `client_http.py` connects to the HTTP endpoint.

## Testing

Start the server:

```bash
uv run server_http.py
```

In another terminal, run:

```bash
uv run client_http.py
```

Verify that the client can list tools and call `search_destinations`.

## Key Takeaways

- Transport determines how MCP messages travel between client and server.
- The same MCP tools can be exposed over different transports.
- Streamable HTTP uses an HTTP endpoint, while stdio uses a local process.
- The HTTP server should be secured appropriately before being exposed beyond the local machine.

## References

- https://py.sdk.modelcontextprotocol.io/run/
- https://py.sdk.modelcontextprotocol.io/client/transports/
- https://modelcontextprotocol.io/
