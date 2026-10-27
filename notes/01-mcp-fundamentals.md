# 01 — MCP Fundamentals

## What Is MCP?

The Model Context Protocol (MCP) is a protocol that standardizes how applications provide context and capabilities to AI applications.

It defines a common way for MCP clients to communicate with MCP servers.

## Core Components

### MCP Host

The application that provides the environment in which an AI model interacts with users and external capabilities.

### MCP Client

The component that establishes a connection to an MCP server and communicates with it using the MCP protocol.

### MCP Server

The component that exposes capabilities such as tools, resources, and prompts.

## Tools

Tools are callable functions exposed by an MCP server.

In this project, `search_destinations` searches for destinations by city and maximum budget.

## Resources

Resources expose information that clients can read, such as documents, catalogs, and application data.

Resources will be explored in the next learning module.

## Prompts

Prompts provide reusable prompt templates that clients can discover and use.

## Current Architecture

```text
Python MCP Client
       |
       | MCP protocol
       v
Travel Assistant MCP Server
       |
       v
search_destinations
       |
       v
In-memory destination data
```

## Key Takeaways

- MCP standardizes communication between clients and servers.
- Tools provide callable capabilities.
- Resources expose information.
- Prompts provide reusable interaction templates.
- MCP itself is not an LLM or an AI agent.

## References

- [MCP Python SDK v2 Documentation](https://py.sdk.modelcontextprotocol.io/v2/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
