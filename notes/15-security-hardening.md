# Lesson 15 — MCP Security Hardening

## Objective

Strengthen input validation, authentication error handling, and security logging in the Travel MCP server.

## Input Validation

The server validates tool inputs before processing them.

- City names must not be empty.
- City names are limited to 100 characters.
- Maximum budget must be a non-negative integer.
- Trip duration must be a positive integer.
- Daily budget and transport cost must be non-negative integers.
- Boolean values are rejected where integer inputs are expected.

## JWT Verification

The Auth0 token verifier checks JWT signatures using the configured JWKS endpoint and restricts accepted algorithms to RS256.

It validates the issuer, audience, and required claims, and requires the `travel:read` scope.

Invalid tokens are rejected. JWKS connection failures are handled without propagating the expected authentication failure to the caller.

## Security Logging

The verifier records safe warning messages for JWT verification failures and JWKS connection failures.

Tests verify that the submitted token strings are not included in these log messages.

## Testing

The test suite covers:

- MCP tool calls, resources, and prompts.
- Invalid trip duration.
- Excessively long city names.
- Boolean values passed as trip duration.
- Invalid JWT rejection.
- JWKS connection failure handling.
- Safe authentication failure logging.

The current test suite passes 15 tests.

## Remaining Considerations

- Review JWKS timeout and caching behavior.
- Confirm that MCP resources and prompts are protected as intended.
- Evaluate whether token resource validation should be enabled.
- Consider input bounds appropriate for the application's operational limits.
- Review client identity validation against the Auth0 token types in use.

## Result

Lesson 15 improves input validation, authentication error handling, and logging safety while preserving the existing MCP server structure.
