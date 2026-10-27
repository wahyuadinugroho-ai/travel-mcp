# Multiple Tools and Structured Output

## Objective

Learn how to register multiple MCP tools and return structured data.

## Implementation

The `travel-mcp` server provides a `calculate_trip_budget` tool.

The tool accepts the trip duration, daily budget, and transportation cost. It returns a structured result containing the input values and calculated total budget.

`TripBudgetResult` defines the output structure using Python's `TypedDict`.

## Key Concepts

- A server can expose multiple tools.
- Type annotations help the SDK generate tool schemas.
- Structured output allows client applications to consume returned data without parsing a text response.
- Clients should check `is_error` before using tool results.

## Testing

Run `uv run client.py`.

Verify that the calculated total budget is correct and that the result is available through `structured_content`.

## References

- https://py.sdk.modelcontextprotocol.io/v2/servers/structured-output/
- https://py.sdk.modelcontextprotocol.io/client/
