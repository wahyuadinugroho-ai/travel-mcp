# Travel MCP

A hands-on learning project exploring the Model Context Protocol (MCP) using Python and the official MCP Python SDK v2.

The goal of this repository is to understand MCP through practical implementations, technical documentation, and incremental experiments.

## Learning Objectives

- Understand MCP architecture and core concepts.
- Build MCP servers and clients using Python.
- Explore tools, resources, and prompts.
- Understand MCP transport mechanisms.
- Implement input validation and error handling.
- Learn MCP security, testing, and deployment practices.

## Tech Stack

- Python 3.11+
- MCP Python SDK v2
- uv
- Git and GitHub

## Current Implementation

### Travel Assistant MCP Server

The first implementation provides a tool for searching travel destinations by city and maximum budget.

**Current features**
- MCP server named `Travel Assistant`
- `search_destinations` tool
- In-memory sample destination data
- Python MCP client
- Tool discovery and invocation
- MCP Inspector testing

### Example Input

```json
{
  "city": "Bali",
  "max_budget": 150000
}
```

### Expected Result

A matching destination, such as Pantai Kuta, with a budget of IDR 100,000.

## Learning Roadmap

- [x] MCP server fundamentals
- [x] MCP client fundamentals
- [ ] MCP resources
- [ ] MCP prompts
- [ ] Multiple tools and structured outputs
- [ ] Error handling and input validation
- [ ] Transport mechanisms
- [ ] Security and authentication
- [ ] Testing and debugging
- [ ] Production readiness

## Project Structure

```text
travel-mcp/
├── server.py
├── client.py
├── pyproject.toml
├── uv.lock
├── README.md
├── LEARNING_LOG.md
├── .gitignore
└── notes/
    └── 01-mcp-fundamentals.md
```

## References

- [MCP Python SDK v2 Documentation](https://py.sdk.modelcontextprotocol.io/v2/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Learning Approach

Each topic follows three steps:

1. Understand the concepts.
2. Implement a working example.
3. Document the implementation, results, challenges, and lessons learned.

This repository will evolve as I explore more MCP capabilities.
