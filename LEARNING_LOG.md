# Learning Log

## 2026-10-27 — MCP Fundamentals

### Objectives

- Understand the fundamentals of MCP Python SDK v2.
- Create an MCP server and client using `uv`.
- Test tool discovery and invocation using MCP Inspector.

### What I Built

- An MCP server named `Travel Assistant`.
- A `search_destinations` tool.
- A Python MCP client.
- A destination search workflow using in-memory data.

### What I Learned

- An MCP server exposes capabilities through protocol primitives such as tools.
- An MCP client can discover available tools and invoke them.
- MCP is a protocol, not an LLM or an AI agent.
- Tools can be invoked programmatically without an LLM.
- `uv` manages project dependencies and executes Python programs.

### Challenges Encountered

- The initial project name conflicted with the third-party package name `mcp`.
- The project was renamed to `travel-mcp` to avoid the conflict.

### Next Steps

- Learn about MCP resources.
- Implement a resource in the existing Travel MCP project.
- Read the resource using an MCP client.
- Document the differences between tools, resources, and prompts.
