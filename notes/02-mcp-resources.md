# MCP Resources

## Objective

Understand how MCP resources expose read-only data to connected clients.

## Implementation

The `travel-mcp` server exposes a resource at `travel://destinations`.

The resource returns the available travel destinations stored by the server.

The client reads the resource using `client.read_resource()`.

## Key Differences

- **Tools** execute operations, such as searching for destinations by city and budget.
- **Resources** expose data that a client can read using a URI.

## Testing

Run the client:

```bash
uv run client.py
```

Verify that the existing search tool still works and that the client can read `travel://destinations`.

## References

- https://py.sdk.modelcontextprotocol.io/client/
- https://py.sdk.modelcontextprotocol.io/servers/
- https://modelcontextprotocol.io/
