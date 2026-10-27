# MCP Prompts

## Objective

Understand how MCP prompts provide reusable message templates to clients.

## Implementation

The `travel-mcp` server exposes a prompt named `plan_trip`.

The prompt accepts three arguments:

- `city`: the destination city.
- `budget`: the total travel budget.
- `days`: the trip duration.

It returns a formatted text template for planning a trip.

## Client Usage

The client uses `list_prompts()` to discover available prompts and `get_prompt()` to render a prompt with arguments.

Prompt arguments are passed as strings.

## Difference Between MCP Primitives

- **Tools** execute operations.
- **Resources** expose data for clients to read.
- **Prompts** provide reusable message templates selected by the user.

## Testing

Run:

```bash
uv run client.py
```

Verify that the `plan_trip` prompt is listed and that the rendered text contains the expected city, budget, and trip duration.

## References

- https://py.sdk.modelcontextprotocol.io/servers/prompts/
- https://py.sdk.modelcontextprotocol.io/client/
- https://modelcontextprotocol.io/
