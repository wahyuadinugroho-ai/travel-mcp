# Testing and Debugging

## Objective

Learn how to test MCP server functionality using pytest and an in-memory MCP client.

## Testing Strategy

Tests connect directly to the MCP server object using `Client(mcp)`. This avoids starting a subprocess or opening a network port.

## Test Coverage

- Destination search returns the expected destination.
- Trip budget calculations return the expected total.
- Invalid trip durations produce tool errors.
- The destinations resource can be read.
- The travel planning prompt can be rendered.

## Running Tests

Run the complete test suite:

```bash
uv run pytest -v
```

## Key Takeaways

- Automated tests make regressions easier to detect.
- In-memory testing is useful for fast server tests.
- Test successful and unsuccessful inputs.
- Keep test expectations aligned with actual server data and SDK result structures.

## References

- https://py.sdk.modelcontextprotocol.io/get-started/testing/
- https://docs.pytest.org/
