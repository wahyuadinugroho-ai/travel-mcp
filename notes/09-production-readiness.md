# Production Readiness

## Objective

Improve the maintainability and observability of the `travel-mcp` project.

## Logging

The server uses Python's standard logging module to record operational events.

Log messages are separate from tool return values.

For stdio transport, avoid writing diagnostic output directly to standard output because it is used for MCP protocol communication.

## Configuration

- Keep project metadata in `pyproject.toml`.
- Use `uv.lock` to maintain reproducible dependency resolution.
- Keep local environments and secrets out of Git.
- Preserve separate entry points for stdio and Streamable HTTP.

## Verification

Run the automated test suite:

```bash
uv run pytest -v
```

Confirm that logging does not change tool results and that existing server capabilities continue to work.

## References

- https://py.sdk.modelcontextprotocol.io/handlers/logging/
- https://py.sdk.modelcontextprotocol.io/run/
- https://py.sdk.modelcontextprotocol.io/
