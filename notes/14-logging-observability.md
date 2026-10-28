# Lesson 14 — Logging & Observability

## Objective

Implement structured application logging for Auth0 token retrieval, retries, and token caching while avoiding sensitive information in logs.

## Logging Levels

- `DEBUG`: Records when a cached access token is reused.
- `INFO`: Records when requesting a token and when token retrieval succeeds.
- `WARNING`: Records temporary HTTP server errors and network transport failures.

## Implementation

The `auth0_client.py` module uses Python's standard `logging` module.

```python
import logging

logger = logging.getLogger(__name__)
```

The implementation records operational events without logging access tokens, client secrets, or complete authentication responses.

### Logged Events

| Event | Level |
|---|---|
| Reusing cached access token | DEBUG |
| Requesting an Auth0 access token | INFO |
| Successfully obtaining a token | INFO |
| Auth0 HTTP error during retry | WARNING |
| Network transport failure | WARNING |

## Testing

Logging behavior is verified with pytest's `caplog` fixture.

The tests verify that:

- A temporary HTTP 500 error is logged before a successful retry.
- Successful token retrieval produces an INFO log.
- Reusing a cached token produces a DEBUG log.
- Access tokens and client secrets are not exposed in the tested log output.

## Security Considerations

- Never log access tokens or client secrets.
- Avoid logging authorization headers or complete token responses.
- Log only the operational details needed to troubleshoot failures.
- Keep retry behavior limited to temporary server errors and transport failures.

## Result

Lesson 14 adds logging observability to the Auth0 token client and tests important logging behavior. The current test suite passes 11 tests.
