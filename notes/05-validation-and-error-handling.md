# Input Validation and Error Handling

## Objective

Learn how to validate tool inputs and handle failed tool calls.

## Implementation

The `travel-mcp` server validates inputs before processing requests.

- The city name cannot be empty.
- The maximum budget cannot be negative.
- The trip duration must be greater than zero.
- Daily budget and transportation cost cannot be negative.

The client checks the tool result's `is_error` field before consuming the output.

## Key Concepts

- Validate input before performing business logic.
- Reject invalid values with clear error messages.
- Distinguish successful tool results from tool errors.
- Test both valid and invalid inputs.

## Testing

Run `uv run client.py`.

Test a valid request and invalid requests such as zero trip days and a negative budget.

Verify that valid requests succeed and invalid requests produce an error result.

## References

- https://py.sdk.modelcontextprotocol.io/
- https://modelcontextprotocol.io/
